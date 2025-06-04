import openpyxl
import datetime
import pandas as pd
import datetime
import jdatetime
from django.contrib.auth import get_user_model
from books.models import Book  


def import_books_from_ods(filepath, user_email):
    try:
        df = pd.read_excel(filepath, engine="odf")
    except Exception as e:
        print(f"❌ خطا در خواندن فایل: {e}")
        return

    User = get_user_model()
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        print(f"❌ کاربر با ایمیل {user_email} پیدا نشد.")
        return

    for idx, row in df.iterrows():
        try:
            title = row["title"]
            body = row["body"]
            author = row["author"]
            translator = row["translator"]
            publisher = row["publisher"]
            category = row["category"]
            page_num = int(row["page_num"]) if not pd.isna(row["page_num"]) else None
            shabak_num = row["shabak_num"]
            year = int(row["year"]) if not pd.isna(row["year"]) else None
            price = float(row["price"])

            if not title or not shabak_num:
                print(f"[⛔ ردیف {idx+2}] title یا shabak_num خالی است.")
                continue

            if Book.objects.filter(shabak_num=shabak_num).exists():
                print(f"[⚠️ تکراری] ردیف {idx+2}: shabak_num {shabak_num}")
                continue

            # تبدیل تاریخ شمسی به میلادی
            try:
                publish_date = jdatetime.date(year, 1, 1).togregorian() if year else None
            except Exception:
                print(f"[⚠️ تاریخ نامعتبر] year={year} در ردیف {idx+2}")
                publish_date = None

            Book.objects.create(
                user=user,
                title=title,
                body=body,
                author=author,
                translator=translator,
                publisher=publisher,
                category=category,
                page_num=page_num,
                shabak_num=shabak_num,
                year=publish_date,
                price=price,
            )

            print(f"[✅ ثبت شد] {title}")
        except Exception as e:
            print(f"[❌ خطا در ردیف {idx+2}] {e}")

    print("🎉 واردسازی کامل شد.")



def import_books_from_excel(filepath, user_email):
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active

    User = get_user_model()
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        print(f"❌ User with email {user_email} not found.")
        return

    for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        title, body, author, translator, publisher, category, page_num, shabak_num, year, price = row

        if not title or not shabak_num:
            print(f"[⛔ رد شد] ردیف {idx}: title یا shabak_num نامعتبر.")
            continue

        if Book.objects.filter(shabak_num=shabak_num).exists():
            print(f"[⚠️ تکراری] ردیف {idx}: shabak_num {shabak_num} قبلاً ثبت شده.")
            continue

        try:
            publish_date = datetime.date(int(year), 1, 1) if year else None
        except ValueError:
            publish_date = None

        book = Book.objects.create(
            user=user,
            title=title,
            body=body,
            author=author,
            translator=translator,
            publisher=publisher,
            category=category,
            page_num=page_num,
            shabak_num=shabak_num,
            year=publish_date,
            price=price
        )

        print(f"[✅ ثبت شد] {title}")

    print("✅ همه کتاب‌ها با موفقیت وارد شدند.")