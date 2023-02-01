from pathlib import Path

from pytestqt.qt_compat import qt_api


class QmlBot:
    def __init__(self) -> None:
        self.engine = qt_api.QtQml.QQmlApplicationEngine()
        main = Path(__file__).parent / "botloader.qml"
        self.engine.load(main.resolve(True))

    @property
    def _loader(self):
        self.root = self.engine.rootObjects()[0]
        return self.root.findChild(qt_api.QtQuick.QQuickItem, "contentloader")

    def load(self, path: Path):
        """
        :returns: `QQuickItem` - the initialized component
        """
        self._loader.setProperty("source", str(path.resolve(True)))
        return self._loader.property("item")

    def loads(self, content: str):
        """
        :returns: `QQuickItem` - the initialized component
        """
        self.comp = qt_api.QtQml.QQmlComponent(
            self.engine
        )  # needed for it not to be collected by the gc
        self.comp.setData(content.encode("utf-8"), qt_api.QtCore.QUrl())
        if self.comp.status() != qt_api.QtQml.QQmlComponent.Status.Ready:
            raise RuntimeError(
                f"component {self.comp} is not Ready:\n"
                f"STATUS: {self.comp.status()}\n"
                f"HINT: make sure there are no wrong spaces.\n"
                f"ERRORS: {self.comp.errors()}"
            )
        self._loader.setProperty("source", "")
        self._loader.setProperty("sourceComponent", self.comp)
        return self._loader.property("item")
