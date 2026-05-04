import fabric # Импортируем Базовый пакет
from fabric import Application # Чтобы запустить, ибо это фундамент всего шелла
from bar import PrimeShellBar
from launcher import PrimeShellLauncher

launcher = PrimeShellLauncher()
bar = PrimeShellBar()

app = Application("PrimeShell", [bar, launcher])

app.set_stylesheet_from_file("style.css")
app.run()