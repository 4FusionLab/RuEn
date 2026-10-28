#include <QApplication>
#include <QCoreApplication>
#include <QEvent>
#include <QKeyEvent>
#include <QMetaObject>
#include <QObject>
#include <QThread>
#include <QWidget>
#include <cstring>
#include <unordered_set>
#include <cstdint>

struct Binding { int key; unsigned int modifiers; };
static std::unordered_set<uint64_t> bindings;
static uint64_t bindingId(int key, unsigned int modifiers) {
    return (static_cast<uint64_t>(modifiers) << 32) | static_cast<unsigned int>(key);
}
extern "C" int ruen_set_bindings(const Binding* entries, int count) {
    auto* app = QCoreApplication::instance();
    if (!app || QThread::currentThread() != app->thread() || count < 0 || (count && !entries)) return -1;
    std::unordered_set<uint64_t> next;
    for (int i = 0; i < count; ++i) next.insert(bindingId(entries[i].key, entries[i].modifiers));
    bindings.swap(next);
    return static_cast<int>(bindings.size());
}

static int latinKey(int key) {
    // Standard Russian and Russian-PC layouts, by physical key position.
    static const char16_t russian[] = u"ФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯ";
    for (int i = 0; i < 26; ++i)
        if (key == russian[i]) return Qt::Key_A + i;
    return 0;
}

class CanvasFilter final : public QObject {
public:
    explicit CanvasFilter(const char* focusClass) : focusClass_(focusClass) {}
    bool eventFilter(QObject* receiver, QEvent* event) override {
        if (sending_ || event->type() != QEvent::KeyPress) return false;
        auto* key = static_cast<QKeyEvent*>(event);
        const int latin = latinKey(key->key());
        if (!latin || key->isAutoRepeat() || !bindings.count(bindingId(latin, static_cast<unsigned int>(key->modifiers())))) return false;
        QWidget* focus = QApplication::focusWidget();
        if (!focus || std::strcmp(focus->metaObject()->className(), focusClass_.constData()) != 0) return false;
        sending_ = true;
        const bool shifted = key->modifiers().testFlag(Qt::ShiftModifier);
        const QChar character(shifted ? latin : latin + ('a' - 'A'));
        QKeyEvent english(QEvent::KeyPress, latin, key->modifiers(), QString(character), false, key->count());
        QCoreApplication::sendEvent(receiver, &english);
        sending_ = false;
        return true;
    }
private:
    QByteArray focusClass_;
    bool sending_ = false;
};
static CanvasFilter* filter = nullptr;
extern "C" int ruen_enable(const char* focusClass) {
    auto* app = QCoreApplication::instance();
    if (!app || QThread::currentThread() != app->thread() || !focusClass) return -1;
    if (filter) return 0;
    filter = new CanvasFilter(focusClass);
    app->installEventFilter(filter);
    return 1;
}
extern "C" int ruen_disable() {
    auto* app = QCoreApplication::instance();
    if (!app || QThread::currentThread() != app->thread()) return -1;
    if (!filter) return 0;
    app->removeEventFilter(filter);
    delete filter; filter = nullptr;
    return 1;
}
