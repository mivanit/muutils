# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: 0.5.1
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Scrape TODO/FIXME/etc comments from source files and generate reports.

Reads configuration from [tool.makefile.inline-todo] in pyproject.toml.
Outputs markdown, jsonl, and html reports with links to source and GitHub issues.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import textwrap
import urllib.parse
import warnings
from dataclasses import asdict, dataclass, field
from functools import reduce
from pathlib import Path
from typing import Any, cast

from jinja2 import Template

try:
	import tomllib  # type: ignore[import-not-found] # pyright: ignore[reportMissingImports]
except ImportError:
	import tomli as tomllib  # type: ignore[import-untyped,import-not-found,no-redef] # pyright: ignore[reportMissingImports]

TOOL_PATH: str = "tool.makefile.inline-todo"


def deep_get(
	d: dict[str, Any],
	path: str,
	default: Any = None,  # noqa: ANN401
	sep: str = ".",
) -> Any:  # noqa: ANN401
	"get a value from a nested dictionary"
	return reduce(
		lambda x, y: x.get(y, default) if isinstance(x, dict) else default,  # function
		path.split(sep) if isinstance(path, str) else path,  # sequence
		d,  # initial
	)


_TEMPLATE_MD_LIST: str = """\
# Inline TODOs

{% for tag, file_map in grouped|dictsort %}
# {{ tag }}
{% for filepath, item_list in file_map|dictsort %}
## [`{{ filepath }}`](/{{ filepath }})
{% for itm in item_list %}
- {{ itm.stripped_title }}  
  local link: [`/{{ filepath }}:{{ itm.line_num }}`](/{{ filepath }}#L{{ itm.line_num }}) 
  | view on GitHub: [{{ itm.file }}#L{{ itm.line_num }}]({{ itm.code_url | safe }})
  | [Make Issue]({{ itm.issue_url | safe }})
{% if itm.context %}
  ```{{ itm.file_lang }}
{{ itm.context_indented }}
  ```
{% endif %}
{% endfor %}

{% endfor %}
{% endfor %}
"""

_TEMPLATE_MD_TABLE: str = """\
# Inline TODOs

| Location | Tag | Todo | GitHub | Issue |
|:---------|:----|:-----|:-------|:------|
{% for itm in all_items %}| [`{{ itm.file }}:{{ itm.line_num }}`](/{{ itm.file }}#L{{ itm.line_num }}) | {{ itm.tag }} | {{ itm.stripped_title_escaped }} | [View]({{ itm.code_url | safe }}) | [Create]({{ itm.issue_url | safe }}) |
{% endfor %}
"""

TEMPLATES_MD: dict[str, str] = dict(
	standard=_TEMPLATE_MD_LIST,
	table=_TEMPLATE_MD_TABLE,
)

TEMPLATE_ISSUE: str = """\
# source

[`{file}#L{line_num}`]({code_url})

# context
```{file_lang}
{context}
```
"""


@dataclass
class Config:
	"""Configuration for the inline-todo scraper"""

	search_dir: Path = Path()
	out_file_base: Path = Path("docs/todo-inline")
	tags: list[str] = field(
		default_factory=lambda: ["CRIT", "TODO", "FIXME", "HACK", "BUG"],
	)
	extensions: list[str] = field(default_factory=lambda: ["py", "md"])
	exclude: list[str] = field(default_factory=lambda: ["docs/**", ".venv/**"])
	context_lines: int = 2
	valid_post_tag: str | list[str] = " \t:<>|[](){{}}"
	valid_pre_tag: str | list[str] = " \t:<>|[](){{}}#"
	tag_label_map: dict[str, str] = field(
		default_factory=lambda: {
			"CRIT": "bug",
			"TODO": "enhancement",
			"FIXME": "bug",
			"BUG": "bug",
			"HACK": "enhancement",
		},
	)
	extension_lang_map: dict[str, str] = field(
		default_factory=lambda: {
			"py": "python",
			"md": "markdown",
			"html": "html",
			"css": "css",
			"js": "javascript",
		},
	)

	templates_md: dict[str, str] = field(default_factory=lambda: TEMPLATES_MD)
	# templates for the output markdown file

	template_issue: str = TEMPLATE_ISSUE
	# template for the issue creation

	template_html_source: Path = Path("docs/resources/templates/todo-template.html")
	# template source for the output html file (interactive table)

	@property
	def template_html(self) -> str:
		"read the html template"
		return self.template_html_source.read_text(encoding="utf-8")

	template_code_url_: str = "{repo_url}/blob/{branch}/{file}#L{line_num}"
	# template for the code url

	@property
	def template_code_url(self) -> str:
		"code url with repo url and branch substituted"
		return self.template_code_url_.replace("{repo_url}", self.repo_url).replace(
			"{branch}",
			self.branch,
		)

	repo_url: str = "UNKNOWN"
	# for the issue creation url

	branch: str = "main"
	# branch for links to files on github

	@classmethod
	def read(cls, config_file: Path) -> Config:
		"read from a file, or return default"
		output: Config
		if config_file.is_file():
			# read file and load if present
			with config_file.open("rb") as f:
				data: dict[str, Any] = cast("dict[str, Any]", tomllib.load(f))  # pyright: ignore[reportUnknownMemberType]

			# try to get the repo url
			repo_url: str = "UNKNOWN"
			try:
				urls: dict[str, str] = {
					k.lower(): v for k, v in data["project"]["urls"].items()
				}
				if "repository" in urls:
					repo_url = urls["repository"]
				if "github" in urls:
					repo_url = urls["github"]
			except Exception as e:
				warnings.warn(
					f"No repository URL found in pyproject.toml, 'make issue' links will not work.\n{e}",
				)

			# load the inline-todo config if present
			data_inline_todo: dict[str, Any] = deep_get(
				d=data,
				path=TOOL_PATH,
				default={},
			)

			if "repo_url" not in data_inline_todo:
				data_inline_todo["repo_url"] = repo_url

			output = cls.load(data_inline_todo)
		else:
			# return default otherwise
			output = cls()

		return output

	@classmethod
	def load(cls, data: dict[str, Any]) -> Config:
		"load from a dictionary, converting to `Path` as needed"
		# process variables that should be paths
		data = {
			k: Path(v)
			if k in {"search_dir", "out_file_base", "template_html_source"}
			else v
			for k, v in data.items()
		}

		# default value for the templates
		data["templates_md"] = {
			**TEMPLATES_MD,
			**data.get("templates_md", {}),
		}

		return cls(**data)


CFG: Config = Config()
# this is messy, but we use a global config so we can get `TodoItem().issue_url` to work


@dataclass
class TodoItem:
	"""Holds one todo occurrence"""

	tag: str
	file: str
	line_num: int
	content: str
	context: str = ""

	def serialize(self) -> dict[str, str | int]:
		"serialize to a dict we can dump to json"
		return {
			**asdict(self),
			"issue_url": self.issue_url,
			"file_lang": self.file_lang,
			"stripped_title": self.stripped_title,
			"code_url": self.code_url,
		}

	@property
	def context_indented(self) -> str:
		"""Returns the context with each line indented"""
		dedented: str = textwrap.dedent(self.context)
		return textwrap.indent(dedented, "  ")

	@property
	def code_url(self) -> str:
		"""Returns a URL to the code on GitHub"""
		return CFG.template_code_url.format(
			file=self.file,
			line_num=self.line_num,
		)

	@property
	def stripped_title(self) -> str:
		"""Returns the title of the issue, stripped of the tag"""
		return self.content.split(self.tag, 1)[-1].lstrip(":").strip()

	@property
	def stripped_title_escaped(self) -> str:
		"""Returns the title of the issue, stripped of the tag and escaped for markdown"""
		return self.stripped_title.replace("|", "\\|")

	@property
	def issue_url(self) -> str:
		"""Constructs a GitHub issue creation URL for a given TodoItem."""
		# title
		title: str = self.stripped_title
		if not title:
			title = "Issue from inline todo"
		# body
		body: str = CFG.template_issue.format(
			file=self.file,
			line_num=self.line_num,
			context=self.context,
			context_indented=self.context_indented,
			code_url=self.code_url,
			file_lang=self.file_lang,
		).strip()
		# labels
		label: str = CFG.tag_label_map.get(self.tag, self.tag)
		# assemble url
		query: dict[str, str] = dict(title=title, body=body, labels=label)
		query_string: str = urllib.parse.urlencode(query, quote_via=urllib.parse.quote)
		return f"{CFG.repo_url}/issues/new?{query_string}"

	@property
	def file_lang(self) -> str:
		"""Returns the language for the file extension"""
		ext: str = Path(self.file).suffix.lstrip(".")
		return CFG.extension_lang_map.get(ext, ext)


def scrape_file(
	file_path: Path,
	cfg: Config,
) -> list[TodoItem]:
	"""Scrapes a file for lines containing any of the specified tags"""
	items: list[TodoItem] = []
	if not file_path.is_file():
		return items
	lines: list[str] = file_path.read_text(encoding="utf-8").splitlines(True)

	# over all lines
	for i, line in enumerate(lines):
		# over all tags
		for tag in cfg.tags:
			# check tag is present
			if tag in line[:200]:
				# check tag is surrounded by valid strings
				tag_idx_start: int = line.index(tag)
				tag_idx_end: int = tag_idx_start + len(tag)
				if (
					line[tag_idx_start - 1] in cfg.valid_pre_tag
					and line[tag_idx_end] in cfg.valid_post_tag
				):
					# get the context and add the item
					start: int = max(0, i - cfg.context_lines)
					end: int = min(len(lines), i + cfg.context_lines + 1)
					snippet: str = "".join(lines[start:end])
					items.append(
						TodoItem(
							tag=tag,
							file=file_path.as_posix(),
							line_num=i + 1,
							content=line.strip("\n"),
							context=snippet.strip("\n"),
						),
					)
				break
	return items


def collect_files(
	search_dir: Path,
	extensions: list[str],
	exclude: list[str],
) -> list[Path]:
	"""Recursively collects all files with specified extensions, excluding matches via globs"""
	results: list[Path] = []
	for ext in extensions:
		results.extend(search_dir.rglob(f"*.{ext}"))

	return [
		f
		for f in results
		if not any(fnmatch.fnmatch(f.as_posix(), pattern) for pattern in exclude)
	]


def group_items_by_tag_and_file(
	items: list[TodoItem],
) -> dict[str, dict[str, list[TodoItem]]]:
	"""Groups items by tag, then by file"""
	grouped: dict[str, dict[str, list[TodoItem]]] = {}
	for itm in items:
		grouped.setdefault(itm.tag, {}).setdefault(itm.file, []).append(itm)
	for tag_dict in grouped.values():
		for file_list in tag_dict.values():
			file_list.sort(key=lambda x: x.line_num)
	return grouped


def main(config_file: Path) -> None:
	"cli interface to get todos"
	global CFG  # noqa: PLW0603
	# read configuration
	cfg: Config = Config.read(config_file)
	CFG = cfg  # pyright: ignore[reportConstantRedefinition]

	# get data
	files: list[Path] = collect_files(cfg.search_dir, cfg.extensions, cfg.exclude)
	all_items: list[TodoItem] = []
	n_files: int = len(files)
	for i, fpath in enumerate(files):
		print(f"Scraping {i + 1:>2}/{n_files:>2}: {fpath.as_posix():<60}", end="\r")
		all_items.extend(scrape_file(fpath, cfg))

	# create dir
	cfg.out_file_base.parent.mkdir(parents=True, exist_ok=True)

	# write raw to jsonl
	with open(cfg.out_file_base.with_suffix(".jsonl"), "w", encoding="utf-8") as f:
		f.writelines(json.dumps(itm.serialize()) + "\n" for itm in all_items)

	# group, render
	grouped: dict[str, dict[str, list[TodoItem]]] = group_items_by_tag_and_file(
		all_items,
	)

	# render each template and save
	for template_key, template in cfg.templates_md.items():
		rendered: str = Template(template).render(grouped=grouped, all_items=all_items)
		template_out_path: Path = Path(
			cfg.out_file_base.with_stem(
				cfg.out_file_base.stem + f"-{template_key}",
			).with_suffix(".md"),
		)
		_ = template_out_path.write_text(rendered, encoding="utf-8")

	# write html output
	try:
		html_rendered: str = cfg.template_html.replace(
			"//{{DATA}}//",
			json.dumps([itm.serialize() for itm in all_items]),
		)
		_ = cfg.out_file_base.with_suffix(".html").write_text(
			html_rendered,
			encoding="utf-8",
		)
	except Exception as e:
		warnings.warn(f"Failed to write html output: {e}")

	print("wrote to:")
	print(cfg.out_file_base.with_suffix(".md").as_posix())


if __name__ == "__main__":
	# parse args
	parser: argparse.ArgumentParser = argparse.ArgumentParser("inline_todo")
	_ = parser.add_argument(
		"--config-file",
		default="pyproject.toml",
		help="Path to the TOML config, will look under [tool.inline-todo].",
	)
	args: argparse.Namespace = parser.parse_args()
	config_file: str = args.config_file
	# call main
	main(Path(config_file))
