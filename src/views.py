import os
import shutil
import uuid
from src.streamGenerator import rawStreamList
from flask import (
    Blueprint,
    render_template,
    current_app,
    request,
    flash,
    redirect,
    send_file
)
from werkzeug.utils import secure_filename, safe_join

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "m3u"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

views = Blueprint("views", __name__)

#download file route
@views.route("/download/<path:filename>")
def download(filename):
    current_directory = os.getcwd()
    downloadDirectory = current_app.config["DOWNLOAD_FOLDER"]
    safePath = safe_join(
        os.path.join(current_directory, r"" + str(downloadDirectory), filename)
    )
    # download the file for user
    return send_file(safePath, as_attachment=True)

# after user downloads the file he is redirected here to delete the file and move back to home page
@views.route("/removefile/<path:filename>")
def removefile(filename):
    current_directory = os.getcwd()
    downloadDirectory = current_app.config["DOWNLOAD_FOLDER"]
    safePath = safe_join(
        os.path.join(current_directory, r"" + str(downloadDirectory), filename)
    )
    os.remove(safePath)
    return redirect("/")


@views.route("/", methods=["GET", "POST"])
def home():
    data = request.data
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        current_directory = os.getcwd()
        if file and allowed_file(file.filename):
            uploadDirectory = current_app.config["UPLOAD_FOLDER"]
            if not os.path.exists(uploadDirectory):
                upload_directory = os.path.join(
                    current_directory, r"" + str(uploadDirectory) + ""
                )
                print(current_directory)
                os.makedirs(upload_directory)
            filename = secure_filename(file.filename)
            filePath = os.path.join(uploadDirectory, filename)
            file.save(filePath)
            print(filePath)
            abc = rawStreamList(filePath)  # generate the stream files

            downloadDirectory = current_app.config["DOWNLOAD_FOLDER"]
            if not os.path.exists(downloadDirectory):
                donwload_directory = os.path.join(
                    current_directory, r"" + str(downloadDirectory)
                )
                os.makedirs(donwload_directory)

            if not os.path.isdir("converted"):
                os.mkdir("converted")
            else:
                shutil.rmtree("converted", ignore_errors=True)
                os.mkdir("converted")
            if os.path.exists("series"):
                shutil.move("series", "converted")
            if os.path.exists("movies"):
                shutil.move("movies", "converted")

            randomFileName = "converted_" + str(uuid.uuid4())
            # zip the generated streams folders
            shutil.make_archive(randomFileName, "zip", "converted")
            # remove the folder after zipping it
            shutil.rmtree("converted", ignore_errors=True)
            # move the ziped file to downloads directory
            zipFileName = randomFileName + ".zip"
            zipFilePath = os.path.join(
                current_directory,
                r"" + str(downloadDirectory) + "/" + zipFileName,
            )
            if not os.path.exists(
                zipFilePath
            ):  # if zip file doesnot exist in download folder then move it
                shutil.move(zipFileName, downloadDirectory)
            else:  # else remove existing zip file then move new one
                os.remove(zipFilePath)
                shutil.move(zipFileName, downloadDirectory)

            return render_template("home.html", filename=zipFileName)
    return render_template("home.html", filename=data)
