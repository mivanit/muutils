def func(*args, **kwargs):
    for arg in args:
        print(f"{type(arg) = }\t{arg = }")
    for key, value in kwargs.items():
        print(f"{type(key) = }\t{key = }\t{type(value) = }\t{value = }")


if __name__ == "__main__":
    import fire  # type: ignore[import]

    fire.Fire(func)
