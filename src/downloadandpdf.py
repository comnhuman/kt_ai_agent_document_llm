import os
import requests
import subprocess
from pathlib import Path
import json
import zipfile

def download_hwp_files(data, download_dir="downloads"):
    """
    JSON 데이터에서 HWP 파일 다운로드
    :param data: JSON 데이터
    :param download_dir: 다운로드 기본 폴더
    :return: 다운로드된 HWP 파일 경로 리스트
    """
    os.makedirs(download_dir, exist_ok=True)
    downloaded_files = []

    for item in data.get("jsonArray", []):
        folder_name = item.get("pblancNm")
        #pblanc_id = item.get("pblancId")
        flpthNm = item.get("flpthNm")
        fileNm = item.get("fileNm")

        if not flpthNm or not fileNm:
            continue

        urls = flpthNm.split("@")
        filenames = fileNm.split("@")

        for url, fname in zip(urls, filenames):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                save_dir = os.path.join(download_dir, folder_name)
                os.makedirs(save_dir, exist_ok=True)
                hwp_path = os.path.join(save_dir, fname)

                with open(hwp_path, "wb") as f:
                    f.write(response.content)

                print(f"✅ 다운로드 성공: {hwp_path}")
                downloaded_files.append(hwp_path)

            except Exception as e:
                print(f"❌ 다운로드 실패: {url} ({e})")
    
    return downloaded_files     


def convert_hwp_to_pdf(hwp_file, output_dir=None):
    """
    HWP 파일을 PDF로 변환
    :param hwp_file: 변환할 HWP 파일 경로
    :param output_dir: PDF 저장 폴더 (None이면 HWP 파일 폴더)
    :return: 변환된 PDF 경로
    """
    if output_dir is None:
        output_dir = str(Path(hwp_file).parent)
    os.makedirs(output_dir, exist_ok=True)

    result = subprocess.run([
        "soffice", "--headless",
        "--infilter=Hwp2002_File",
        "--convert-to", "pdf:writer_pdf_Export",
        "--outdir", output_dir,
        hwp_file
    ], capture_output=True)

    if result.returncode != 0:
        raise RuntimeError(f"HWP -> PDF 변환 실패: {result.stderr.decode('utf-8')}")

    pdf_path = Path(output_dir) / (Path(hwp_file).stem + ".pdf")
    return str(pdf_path)

def handle_zip(file_path, pdf_output_dir):    #zip파일 전용 핸들러 (파일 이름 한글 깨짐 방지 위함)
    pdf_files = []
    extract_dir = Path(file_path).with_suffix("")
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(file_path) as zf:
        for info in zf.infolist():
            try:
                # 한글 깨짐 방지
                try:
                    filename = info.filename.encode('cp437').decode('euc-kr')
                except UnicodeDecodeError:
                    filename = info.filename

                extracted_path = extract_dir / Path(filename).name
                with open(extracted_path, "wb") as f:
                    f.write(zf.read(info.filename))

                # PDF 변환
                try:
                    pdf_file = convert_hwp_to_pdf(str(extracted_path), pdf_output_dir)
                    pdf_files.append(pdf_file)
                    print(f"✅ ZIP 안 PDF 변환 완료: {pdf_file}")
                except Exception as e:
                    print(f"❌ ZIP 안 PDF 변환 실패: {extracted_path} ({e})")

            except Exception as e:
                print(f"❌ ZIP 압축 해제 실패: {info.filename} ({e})")
    
    return pdf_files

def download_and_convert(data, download_dir="downloads", pdf_output_dir="변환된 pdf"):
    """
    Wrapper function
    JSON에서 HWP 파일 다운로드 후 PDF로 변환
    :param data: JSON 데이터
    :param download_dir: HWP 다운로드 기본 폴더
    :param pdf_output_dir: PDF 저장 폴더 
    :return: 변환된 PDF 경로 리스트
    """
    all_pdf_files = []
    downloaded_files = download_hwp_files(data, download_dir)

    for file_path in downloaded_files:
        ext = Path(file_path).suffix.lower()
        try:
            # 원본 파일이 있는 폴더명
            original_folder = Path(file_path).parent.name
            # PDF 저장 폴더: pdf_output_dir / original_folder
            save_pdf_dir = Path(pdf_output_dir) / original_folder
            os.makedirs(save_pdf_dir, exist_ok=True)


            if ext == ".zip":
                pdf_files = handle_zip(file_path, str(save_pdf_dir))
                all_pdf_files.extend(pdf_files)
            else:
                pdf_file = convert_hwp_to_pdf(file_path, str(save_pdf_dir))
                all_pdf_files.append(pdf_file)
                print(f"✅ PDF 변환 완료: {pdf_file}")
        except Exception as e:
            print(f"❌ 변환 실패: {file_path} ({e})")
    
    return all_pdf_files



#메인 함수. KT LLM이 적절 사업 json 목록을 보내면 그게 data 변수에 들어가면 된다

if __name__ == "__main__":
    with open("경영_support_programs.json", "r", encoding="utf-8") as f:     #데모를 위해 .json파일을 열었음. 나중에 main.py에서 받아올 예정
        data = json.load(f)

# jsonArray 확인
items = data.get("jsonArray", [])

#os.makedirs("downloads", exist_ok=True).  #src 폴더에 저장할거면 수정하면 됨

# 필요한 필드만 추출
result = []
for item in items:
    filtered = {
        "pblancNm": item.get("pblancNm"),
        "flpthNm": item.get("flpthNm") or item.get("printFlpthNm"),  # 둘 중 하나 존재하면 사용. 간혹가다 한쪽이 none 인 경우 좀 있음.
        "fileNm": item.get("fileNm") or item.get("printFileNm")
    }
    result.append(filtered)
pdf_list = download_and_convert(data)
print("모든 PDF 변환 완료:", pdf_list)








