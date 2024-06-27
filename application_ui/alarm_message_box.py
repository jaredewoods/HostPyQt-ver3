from PyQt6.QtWidgets import QMessageBox
from resources.alarm_dict import alarm_dict


class AlarmMessageBox:

    @staticmethod
    def show_alarm_messagebox(alarm, subcode):
        alarm_data = alarm_dict.get(alarm, None)

        if alarm_data is None:
            alarm_info = {
                "Message": "Unknown message",
            }
        else:
            alarm_info = next(iter(alarm_data.values()), {
                "Message": "Unknown message",
                "Cause": "Unknown cause",
                "Potential Causes": ["Unknown potential causes"]
            })

        message = alarm_info.get("Message", "Unknown message")
        cause = alarm_info.get("Cause", "Unknown cause")
        potential_causes = alarm_info.get("Potential Causes", ["Unknown potential causes"])
        potential_causes_formatted = "\n".join([f"• {cause}" for cause in potential_causes])
        formatted_message = (
            f"Alarm: {alarm}\n\n"
            f"{message}\n\n"
            f"{cause}\n\n"
            f"Potential Causes:\n{potential_causes_formatted}\n\n"
            f"Subcode: {subcode}"
        )

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Alarm Detected")
        msg.setInformativeText(formatted_message)
        msg.setWindowTitle("Alarm")
        msg.exec()
