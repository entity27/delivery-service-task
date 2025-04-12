import pkgutil


def autoimport_models(
    ignore: tuple[str, ...] = ('config', 'backgrounds', 'utils'),
    base: str | None = 'src',
) -> None:
    """
    Ищем внутри доменов модели и импортируем их, чтобы alembic их обнаружил из метадаты
    """
    to_ignore = set(ignore)
    for module in pkgutil.iter_modules(['src']):
        if module.name in to_ignore:
            continue
        for submodule in pkgutil.iter_modules([f'src/{module.name}']):
            if submodule.name != 'models':
                continue
            if base is None:
                to_import = f'{module.name}.{submodule.name}'
            else:
                to_import = f'{base}.{module.name}.{submodule.name}'
            __import__(to_import)
