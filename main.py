# готовый ScrButton
# заготовки FirstScr, SecondScr, ThirdScr, FourthScr
# переход работает
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from seconds import *
from sits import *
from runner import *
from scrollLabel import *
from instructions import *
from ruffier import *

#Нужные данные
age = 0
name = ''
pulse1 = 0
pulse2 = 0
pulse3 = 0

#Функция получения результаты
def get_result():
    res = test(pulse1, pulse2, pulse3, age)
    return name + '\n' + res[0] + '\n' + res[1] 

#Класс для пролистывания текста
class ScrButton(Button):
    def __init__(self,screen,direction = 'right', goal = 'main', **params):
        super().__init__(**params)
        self.screen = screen
        self.direction = direction
        self.goal = goal

#Функция нажатия
def on_press(self):
    self.screen.manager.transition.direction = self.direction
    self.screen.manager.current = self.goal
    
class MainScr(Screen):
    def __init__(self, name = 'main'):
        super().__init__(name=name)
        hor_layout = BoxLayout()

        scroll_text = ScrollLabel(txt_instruction)

        name_lab = Label(text = "Ваше имя: ")
        self.name_value = TextInput(text='', multiline = False)

        age_lab = Label(text = "Ваш возраст: ")
        self.age_value = TextInput(text='7', multiline = False)

        btn_next = Button(text = "Вперед", size_hint=(1,0.2))
        btn_next.on_press = self.next

        hor_layout1 = BoxLayout(size_hint=(1,0.2))
        hor_layout1.add_widget(name_lab)
        hor_layout1.add_widget(self.name_value)

        hor_layout2 = BoxLayout(size_hint=(1,0.2))
        hor_layout2.add_widget(age_lab)
        hor_layout2.add_widget(self.age_value)

        ver_layout = BoxLayout(orientation = 'vertical')
        ver_layout.add_widget(scroll_text)
        ver_layout.add_widget(hor_layout1)
        ver_layout.add_widget(hor_layout2)
        ver_layout.add_widget(btn_next)

        self.add_widget(ver_layout)

    def next(self):
        global name,age
        name = self.name_value.text
        age = int(self.age_value.text)
        self.manager.current = 'first'

class FirstScr(Screen):
    def __init__(self, name='first'):
        super().__init__(name=name)

        self.next_screen = False

        hor_layout = BoxLayout()

        scroll_text = ScrollLabel(txt_test1)
        scroll_text2 = ScrollLabel("Считайте пульс")

        self.sec = Seconds(15)
        self.sec.bind(done = self.sec_finished)

        result_lab = Label(text = "Введите результат: ")
        self.result_value = TextInput(text='0', multiline = False)
        self.result_value.set_disabled(True)

        self.but = Button(text = "Начать", size_hint=(1,0.2))
        self.but.background_color = (0,0.9,0.5,1)
        self.but.on_press = self.next

        hor_layout1 = BoxLayout(size_hint=(1,0.2))
        hor_layout1.add_widget(result_lab)
        hor_layout1.add_widget(self.result_value)
        ver_layout = BoxLayout(orientation = 'vertical')
        ver_layout.add_widget(scroll_text)
        ver_layout.add_widget(scroll_text2)
        ver_layout.add_widget(self.sec)
        ver_layout.add_widget(hor_layout1)
        ver_layout.add_widget(self.but)

        self.add_widget(ver_layout)

    def sec_finished(self, *args):
        self.but.set_disabled(False)
        self.but.text = "Продолжить"
        self.result_value.set_disabled(False)
        self.next_screen = True

    
    def next(self):
        if self.next_screen == False:
            self.sec.start()
            self.but.set_disabled(True)
        else:
            global pulse1
            pulse1 = int(self.result_value.text)
            self.manager.current = 'second'


class SecondScr(Screen):
    def __init__(self, name='second'):
        super().__init__(name=name)
        
        self.next_screen = False
        instr = ScrollLabel(txt_sits, size_hint = (1,0.2))

        self.sits_value = Sits(30,size_hint=(1,0.2))
        self.run = Runner(total = 30, steptime = 1.5)
        self.run.bind(finished = self.run_finished)

        self.but = Button(text = "Начать", size_hint=(1,0.2))
        self.but.on_press = self.next

        ver = BoxLayout(orientation = "vertical")
        ver.add_widget(instr)
        ver.add_widget(self.sits_value)
        ver.add_widget(self.run)
        ver.add_widget(self.but)

        self.add_widget(ver)

    def next(self):
        if self.next_screen == False:
            self.but.set_disabled(True)
            self.run.start()
            self.run.bind(value = self.sits_value.next)
        else:
            self.manager.current = 'third'

    def run_finished(self,*args):
        self.next_screen = True
        self.but.text = "Продолжить"
        self.but.set_disabled(False)

class ThirdScr(Screen):
    def __init__(self, name='third'):
        super().__init__(name=name)
        self.next_screen = False
        self.stage = 0
 
        instr1 = ScrollLabel(txt_test3)
        self.instr2 = ScrollLabel('Считайте пульс')
        
        self.sec = Seconds(15)
        self.sec.bind(done = self.sec_finished)
        
        res1_label = Label(text='Результат:')
        self.res1_value = TextInput(text='0')
        self.res1_value.set_disabled(True)
        res2_label = Label(text='Результат после отдыха:')
        self.res2_value = TextInput(text='0')
        self.res2_value.set_disabled(True)
        self.but = Button(text='Начать',size_hint=(1,0.2))
        self.but.on_press = self.next
 
        hor1 = BoxLayout(size_hint=(1,0.2))
        hor1.add_widget(res1_label)
        hor1.add_widget(self.res1_value)
        hor2 = BoxLayout(size_hint=(1,0.2))
        hor2.add_widget(res2_label)
        hor2.add_widget(self.res2_value)
        ver = BoxLayout(orientation = 'vertical')
        ver.add_widget(instr1)
        ver.add_widget(self.instr2)
        ver.add_widget(self.sec)
        ver.add_widget(hor1)
        ver.add_widget(hor2)
        ver.add_widget(self.but)
        self.add_widget(ver)

 
    def sec_finished(self, instance, value):
        if value:
            self.stage += 1
            if self.stage == 1:
                self.instr2.set_text('Отдыхайте')
                self.sec.restart(30)
                self.res1_value.set_disabled(False)
            elif self.stage == 2:
                self.instr2.set_text('Считайте пульт')
                self.sec.restart(15)

            elif self.stage == 3:
                self.res2_value.set_disabled(False)
                self.but.text = 'Завершить'
                self.but.set_disabled(False)
                self.next_screen = True
    def next(self):
        if self.next_screen == False:
            self.but.set_disabled(True)
            self.sec.start()
        else:
            global pulse2, pulse3
            pulse2 = int(self.res1_value.text)
            pulse3 = int(self.res2_value.text)
            self.manager.current = 'fourth'

class FourthScr(Screen):
    def __init__(self, name='fourth'):
        super().__init__(name=name)
        ver = BoxLayout(orientation='vertical', padding=8, spacing=8)
        self.instr = ScrollLabel('')

        ver.add_widget(self.instr)
        self.add_widget(ver)
 
        self.on_enter = self.before


    def before(self):
 
        self.instr.set_text(get_result())


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScr(name='main'))
        sm.add_widget(FirstScr(name='first'))
        sm.add_widget(SecondScr(name='second'))
        sm.add_widget(ThirdScr(name='third'))
        sm.add_widget(FourthScr(name='fourth'))

        return sm

MyApp().run()
