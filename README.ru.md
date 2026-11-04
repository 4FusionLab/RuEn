<h1 align="center">RuEn для Autodesk Fusion</h1>
<p align="center"><strong>Горячие клавиши Fusion работают и на русской раскладке.</strong><br>Используйте назначенные сочетания клавиш Fusion 360 без переключения клавиатуры на английский язык.</p>

<p align="center"><a href="https://github.com/4FusionLab/RuEn/releases/latest"><strong>Скачать RuEn</strong></a> · <a href="README.md">English</a> · <a href="https://github.com/4FusionLab/RuEn/issues">Сообщить о проблеме</a></p>

**RuEn** — аддон Autodesk Fusion для работы с горячими клавишами в русской раскладке на macOS и Windows. Он считывает назначения `HotKey.List` и сопоставляет русские клавиши с соответствующими латинскими; сами назначения Fusion не изменяются.

## Как это работает

Поддерживаются зарегистрированные сочетания с одной латинской буквой и модификаторами, пока фокус находится в `QTCanvas`. Символьные и многошаговые сочетания не поддерживаются.

После изменения назначений выполните **RuEn: обновить хоткеи**. Команда **RuEn: включить / выключить** управляет фильтром.

## Поддержка и ограничения

- **macOS:** Apple Silicon.
- **Windows:** x64.
- **Горячие клавиши:** зарегистрированные буквенные сочетания с модификаторами.
- **Не поддерживается:** последовательности из нескольких шагов и сочетания с символьными клавишами.

Фильтр использует внутренний класс Fusion `QTCanvas` и Qt, а не публичный API Autodesk; совместимость с будущими версиями Fusion не гарантируется.

## Установка

1. Скачайте [последний релиз](https://github.com/4FusionLab/RuEn/releases/latest): `universal` для обеих ОС, `macos` для macOS Apple Silicon или `windows` для Windows x64. Универсальный архив выбирает библиотеку по ОС автоматически.
2. Распакуйте архив, сохранив папку `RuEn` и её содержимое. Не перемещайте отдельные файлы из неё.
3. В Fusion откройте **Utilities → Add-Ins → Scripts and Add-Ins**, выберите **+ → Script or add-in from device** и укажите папку `RuEn`.
4. Выберите **RuEn → Run** и включите **Run on Startup**, чтобы аддон запускался вместе с Fusion.
5. Используйте назначенные сочетания в рабочей области Design при русской раскладке.

**Обновляете RuEnProbe?** Остановите старый аддон в Scripts and Add-Ins, отключите его автозапуск и удалите старую запись, прежде чем добавить RuEn. Не запускайте обе копии одновременно. Идентификатор manifest сохранён, пользовательские назначения Fusion не изменяются.

Для удаления остановите RuEn, отключите **Run on Startup**, удалите его запись в Fusion и распакованную папку. При ошибке загрузки проверьте соответствие архива ОС и наличие библиотеки рядом с `RuEn.py`.

## Разработка

Python-код находится в [`RuEn/`](RuEn/), нативный фильтр — в [`native/ruen_filter.cpp`](native/ruen_filter.cpp). `python scripts/package.py` создаёт три ZIP в `dist/` из имеющихся библиотек; он не пересобирает их. Для macOS используйте `scripts/build_macos.sh` с `QT_SDK` для Qt 6.8.3; для Windows — `scripts/build_windows.ps1` в окружении MSVC x64 с совместимым Qt SDK (Qt 6.8.1). `experiments/native_filter_test.py` использует отдельное окружение PySide и не входит в поставку.

## Другие аддоны Fusion 360 от 4FusionLab

[Perfora — перфорация и узоры отверстий](https://github.com/4FusionLab/Perfora) · [Selectra — выбор похожих граней и рёбер](https://github.com/4FusionLab/Selectra) · [Ejix — извлечение объёмов](https://github.com/4FusionLab/Ejix) · [Planara — будущая развёртка поверхностей](https://github.com/4FusionLab/Planara)

[Заметки к релизу](RELEASE_NOTES.md) · [Лицензия](LICENSE) · [4FusionLab](https://github.com/4FusionLab)

<sub>Независимый проект, не связанный с Autodesk и не одобренный ею.</sub>
