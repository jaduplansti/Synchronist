import flet as ft;
import time;
import requests;
import bcrypt;
import json;
import pyfiglet;

GAME_URL = "http://localhost:5000";

class Client(): # TODO: handle resize event 
  def __init__(self):
    self.states = {}
    
  def percent(self, n, total):
    return (n / 100) * total;
   
class ChatMenu(ft.UserControl):
  def __init__(self, page):
    super().__init__();
    self.page = page;
    self.menu = ft.Ref[ft.Container]();
    self.chats = ft.Ref[ft.Column]();
    self.text_field = ft.Ref[ft.TextField]();
  
  def clear_text_field(self):
    self.text_field.current.value = "";
    self.page.update(self.menu.current);
  
  def handle_input(self, msg):
    msg = msg.split(" ");
    match msg[0]:
      case "register":
        info = ' '.join(msg[1:]).split(",");
        if len(info) < 2:
          self.add_text("missing a password/username, try 'register (name), (password)'", ft.colors.RED);
        else:
          ret = requests.post("{url}/register".format(url = GAME_URL), json.dumps({"name" : info[0], "passw" : str(bcrypt.hashpw(info[1].encode(), bcrypt.gensalt()))}));
          match ret.content.decode():
            case "1":
              self.add_notice("register success!");
            case "-3":
              self.add_error("oops. register fail!");
            case "-1":
              self.add_error("player already exists, try a different name.");
      case "map":
        map = requests.get("{url}/map".format(url = GAME_URL));
        self.add_text(map.content.decode(), ft.colors.WHITE);
          
  def send(self, event):
    text = event.control.value;
    self.clear_text_field();
    self.add_text("you > {text}".format(text = text), ft.colors.WHITE);
    self.handle_input(text);
  
  def add_error(self, msg):
    self.add_text(msg, ft.colors.RED);
    
  def add_notice(self, msg):
    self.add_text(msg, ft.colors.YELLOW);
    
  def build(self):
    chats = ft.Column(ref = self.chats, spacing = 0,  height = client.percent(90, self.page.height), width = self.page.height, scroll = True, auto_scroll = True);
    chatField = ft.TextField(ref = self.text_field, label = "command", bgcolor = ft.colors.GREY, on_submit = self.send);
    chatCol = ft.Column(controls = [chats, chatField]);
    chatMenu = ft.Container(ref = self.menu, bgcolor = ft.colors.BLACK, content = chatCol, width = self.page.width, height = self.page.height,
    border_radius = 15);
    return chatMenu;
  
  def add_text(self, text, color):
    self.chats.current.controls.append(ft.Text(text, color = color, size = 18));
    self.page.update(self.menu.current);
  
def main(page : ft.Page):
  chatMenu = ChatMenu(page);
  page.add(chatMenu);
  if page.client_storage.contains_key("account"):
    pass;
  else:
    chatMenu.add_text(pyfiglet.figlet_format("Synchro-nist", font = "5lineoblique"), ft.colors.WHITE);
    chatMenu.add_text("Welcome To Synchronist\nType 'register (name), (password)' to get started", ft.colors.YELLOW);

client = Client();    
ft.app(target = main, view = ft.AppView.WEB_BROWSER, port = 8000);