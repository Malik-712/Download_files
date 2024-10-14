from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

# مسارات المجلدات
uplink_directory = r"C:\Users\عبدالملك الجنيدل\OneDrive\Desktop\uplink"
download_folder = os.path.join(uplink_directory, "Downloads")
upload_folder = os.path.join(uplink_directory, "Download_files")  # تم التغيير هنا

# تأكد من أن المجلدات موجودة
os.makedirs(upload_folder, exist_ok=True)
os.makedirs(download_folder, exist_ok=True)

# توجيه الملفات الثابتة
app.mount("/static", StaticFiles(directory=os.path.join(uplink_directory, "static")), name="static")

# الصفحة الرئيسية
@app.get("/")
async def home():
    return FileResponse(os.path.join(uplink_directory, "main.html"))

# صفحة الإدارة
@app.get("/admin")
async def admin():
    return FileResponse(os.path.join(uplink_directory, "admin.html"))

# صفحة تنزيل الملفات
@app.get("/blank")
async def blank():
    return FileResponse(os.path.join(uplink_directory, "blank.html"))

# رفع الملفات
@app.post("/upload")
async def upload_file(files: list[UploadFile] = File(...)):
    # رفع الملفات للمجلد المؤقت
    for file in files:
        file_location = os.path.join(upload_folder, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())

    return {"message": f"تم رفع {len(files)} ملف(ات)"}

# حساب عدد الملفات في مجلد الرفع فقط
@app.get("/file-count")
async def file_count():
    count = len(os.listdir(upload_folder))
    return {"file_count": count}

# تنزيل المجلد الذي يحتوي على الملفات ثم حذف الملفات
@app.get("/download")
async def download_folder(folderName: str = Query(..., description="اسم المجلد الذي سيتم إنشاؤه")):
    # تأكد من وجود الملفات
    if len(os.listdir(upload_folder)) == 0:
        return JSONResponse(content={"error": "لا توجد ملفات لتنزيلها"}, status_code=404)

    # إنشاء مجلد باسم المستخدم في التنزيلات
    target_folder = os.path.join(download_folder, folderName)
    os.makedirs(target_folder, exist_ok=True)

    # نسخ الملفات إلى المجلد الجديد
    for file_name in os.listdir(upload_folder):
        source_file = os.path.join(upload_folder, file_name)
        target_file = os.path.join(target_folder, file_name)
        shutil.copy2(source_file, target_file)

    # حذف الملفات الأصلية من مجلد الرفع وإعادة تعيينه
    for file_name in os.listdir(upload_folder):
        os.remove(os.path.join(upload_folder, file_name))

    return JSONResponse(content={"message": f"تم تنزيل المجلد '{folderName}' في التنزيلات وتم حذف الملفات"}, status_code=200)

# تشغيل الخادم باستخدام Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.68.125", port=2000)
