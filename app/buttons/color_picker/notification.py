from sys import platform
if platform == 'win32':
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
else:
    import subprocess
    import os
    import pyperclip


def toast(display_type, typestocopy, color_names_final):
    duration = 5
    if platform != 'win32':
        unix_icon = os.getcwd()+"/static/icons/icon.png"
        print(unix_icon)
        message_body = dict(color_names_final) # this ensures we have a copied dictionary, not a reference to the original.
        del message_body["NAME"]
        message_body = str(message_body).replace("', ", ",\n")[:-2][2:].replace("'", "")
        subprocess.Popen(["notify-send", "-t", str(duration*1000), "-i", str(unix_icon), "--app-name", "WebDeck", str(color_names_final["NAME"]), str(message_body)])
        return
        ### TODO COPY VALUE TO CLIPBOARD (add config option which value(s) should be copied)
        """pyperclip.copy(which value?)
        """
    icon = "static\\icons\\icon.ico"
    message = ""
    if display_type and display_type.lower() != "list":
        message = (
            list(color_names_final.values())[0]
            if typestocopy and len(typestocopy.split(";")) == 1
            else ", ".join(color_names_final.values())
        )
    elif typestocopy and len(typestocopy.split(";")) == 1:
        message = str(color_names_final)[:-2][2:].replace("'", "")
    else:
        message = (
            str(color_names_final)
            .replace("', ", ",\n")[:-2][2:]
            .replace("'", "")
        )

    title = "WebDeck Color Picker"
    toaster.show_toast(
        title, message, icon_path=icon, duration=duration, threaded=True
    )
