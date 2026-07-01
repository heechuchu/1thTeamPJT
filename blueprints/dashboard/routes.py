from flask import Blueprint, render_template, request, Response, url_for, redirect
from utils.json_manager import (
    load_settings,
    save_settings,
    load_logs,
    add_log
)
dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
def dashboard():
    return render_template(
        "dashboard/dashboard.html",
        today_count=0,
        warning_message="현재 위험 없음",
        logs=[]
    )


@dashboard_bp.route("/live")
def live():
    return render_template(
        "dashboard/live.html",
        detect_time="감지 없음"
    )


@dashboard_bp.route("/logs")
def logs():

    log_type = request.args.get("type", "all")

    logs = load_logs()

    if log_type != "all":
        logs = [
            log for log in logs
            if log["type"] == log_type
        ]

    return render_template(
        "dashboard/logs.html",
        logs=logs,
        selected_type=log_type
    )


@dashboard_bp.route("/statistics")
def statistics():
    return render_template(
        "dashboard/statistics.html",
        today_count=0,
        week_count=0,
        month_count=0,
        total_count=0,
        labels=["월", "화", "수", "목", "금"],
        values=[0, 0, 0, 0, 0],
        type_labels=["침입", "움직임", "기타"],
        type_values=[0, 0, 0],
        hour_labels=["00시", "03시", "06시", "09시", "12시", "15시", "18시", "21시"],
        hour_values=[0, 1, 2, 1, 3, 5, 2, 1]
    )


@dashboard_bp.route("/settings")
def settings():

    settings_data = load_settings()

    return render_template(
        "dashboard/settings.html",
        settings=settings_data
    )


@dashboard_bp.route("/settings/save", methods=["POST"])
def settings_save():

    settings_data = {
        "danger_zone_enabled": request.form.get("danger_zone_enabled"),
        "sensitivity": request.form.get("sensitivity"),
        "alert_enabled": request.form.get("alert_enabled"),
        "save_video": request.form.get("save_video")
    }

    save_settings(settings_data)

    return redirect(url_for("dashboard.settings"))


@dashboard_bp.route("/video_feed")
def video_feed():

    return Response(
        generate_dummy_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


def generate_dummy_frames():

    while True:
        frame = """
        <svg xmlns="http://www.w3.org/2000/svg" width="900" height="500">
            <rect width="100%" height="100%" fill="#020617"/>
            <text x="50%" y="45%" text-anchor="middle" fill="#38bdf8" font-size="32">
                DRONE CAMERA READY
            </text>
            <text x="50%" y="55%" text-anchor="middle" fill="#94a3b8" font-size="18">
                ESP32-CAM / OpenCV 연결 예정
            </text>
        </svg>
        """.encode("utf-8")

        yield (
            b"--frame\r\n"
            b"Content-Type: image/svg+xml; charset=utf-8\r\n\r\n"
            + frame
            + b"\r\n"
        )

@dashboard_bp.route("/test/add_log")
def test_add_log():

    add_log(
        log_type="intrusion",
        type_name="위험구역 침입",
        location="A구역",
        status="처리 완료"
    )

    return "OK"