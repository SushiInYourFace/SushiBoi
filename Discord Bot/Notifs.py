from pynotifier import Notification

def send(content):
    Notification(title='New Notification from SushiBot', description=content).send()