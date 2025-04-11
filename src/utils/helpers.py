import pkgutil


def autoimport_models(
    ignore: tuple[str, ...] = ('config', 'backgrounds', 'utils'),
) -> None:
    """
    Ищем внутри доменов модели и импортируем их, чтобы alembic их обнаружил из метадаты
    """
    to_ignore = set(ignore)
    for module in pkgutil.iter_modules(['src']):
        if module.name in to_ignore:
            continue
        for submodule in pkgutil.iter_modules([f'src/{module.name}']):
            if submodule.name == 'models':
                __import__(f'{module.name}.{submodule.name}')
