"""
importing library for my project
"""

from tkinter import *
from PIL import Image, ImageTk
from sqlite3 import *

"""
create my tables with SQL
"""


# cu.execute("CREATE TABLE books (book_id integer primary key autoincrement,title text,birthday date,genre text,avablecopies integer )")
# cu.execute("create table members(member_id integer primary key autoincrement,name text,address text,phonenumber integer  ,join_date date,age integer) ")
# cu.execute("""create table loans(
#             loan_id integer primary key autoincrement,
#             book_id integer,
#             member_id integer ,
#             loan_date date,
#             return_date date)""")
# cu.execute("Create table admins(admin_first_name text primary key,admin_password text  )")

class MultiPageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Page App")

        self.container = Frame(self.root, background="lightblue")
        self.container.pack(fill=BOTH, expand=True)

        self.page1 = Page1(self.container, self)
        self.page2 = Page2(self.container, self)
        self.page3 = Page3(self.container, self)
        self.page4 = Page4(self.container, self)
        self.page5 = Page5(self.container, self)
        self.page1.grid(row=0, column=0, sticky='nsew')
        self.page2.grid(row=0, column=0, sticky='nsew')
        self.page3.grid(row=0, column=0, sticky='nsew')
        self.page4.grid(row=0, column=0, sticky='nsew')
        self.page5.grid(row=0, column=0, sticky='nsew')
        self.show_frame(self.page1)

    def show_frame(self, page):
        page.tkraise()


class Page1(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        image_visible = Image.open("cheat.jpg")
        image_hidden = Image.open("hide.jpg")
        photo_visible = ImageTk.PhotoImage(image_visible)
        photo_hidden = ImageTk.PhotoImage(image_hidden)

        show_password = BooleanVar(value=False)

        def sign_in():
            p = password_Entry.get()
            u = Username_Entry.get()
            conn = connect("Library.db")
            cu = conn.cursor()
            cu.execute("select * from admins where admin_first_name=? AND admin_password=?", (u, p))  # noqa
            result = cu.fetchall()
            if result and p != '' and u != "":
                controller.show_frame(controller.page2)

        def toggle_password():
            if show_password.get():
                password_Entry.config(show='*')
                show.config(image=photo_hidden)
            else:
                password_Entry.config(show='')
                show.config(image=photo_visible)

        def mojavez():
            conn = connect("Library.db")
            cu = conn.cursor()
            cu.execute("select * from admins where admin_first_name=? ",  # noqa
                       (Username_Entry.get(),))  # noqa
            result = cu.fetchall()

            return not result

        def add_admin():
            new_password = password_Entry.get()
            new_username = Username_Entry.get()
            conn = connect("Library.db")
            cu = conn.cursor()

            if mojavez() and new_username != "" and new_password != "":
                cu.execute("insert into admins values (?,?)", (Username_Entry.get(), password_Entry.get()))  # noqa
                helper.set("admin added")
                conn.commit()
            else:
                helper.set("admin already exist ")

            conn.close()

        helper = StringVar()
        Username = Label(self, text="Username", bg="lightblue", fg="red", font=(10), width=10)
        Username.grid(row=1, column=0, padx=600, pady=300)

        help = Label(self, textvariable=helper, fg="red")
        help.place(x=600, y=280)
        password = Label(self, text="password", bg="lightblue", fg="red", font=(10), width=10)
        password.place(x=600, y=350)

        password_Entry = Entry(self)
        password_Entry.place(x=720, y=350)

        Username_Entry = Entry(self)
        Username_Entry.place(x=720, y=300)
        image = Image.open("show.jpg")
        photo = ImageTk.PhotoImage(image)
        show = Label(self, image=photo)
        show.place(x=660, y=150)

        sign_in = Button(self, text="sign in", command=sign_in)
        sign_in.place(x=690, y=400)

        checkbox = Checkbutton(self, text="hide Password", variable=show_password, command=toggle_password,
                               bg="lightblue")
        checkbox.place(x=840, y=350)

        new_admin = Button(self, text="add admin", fg="blue", relief="flat", command=add_admin)
        new_admin.place(x=690, y=450)


class Page2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        data_mem = StringVar()
        data_lon = StringVar()
        data_bok = StringVar()
        rep_ = StringVar()
        bol = BooleanVar(value=True)
        bol2 = BooleanVar(value=True)

        def loan_search():
            conn = connect("Library.db")
            cu = conn.cursor()
            cu.execute("select * from loans where loan_id = ?", (search_e.get(),))  # noqa
            result = cu.fetchall()
            if result:
                for i in result:
                    rep_.set(
                        f"loan_id:{i[0]}\n book_id:{i[1]}\n member_id:{i[2]}\n loan_date:{i[3]}\n return_date:{i[4]}")
            else:
                rep_.set("loan not found")

        def count_mem():
            conn = connect("Library.db")
            cu = conn.cursor()
            cu.execute("select count(*) from members")  # noqa
            result = cu.fetchall()
            for i in result:
                data_mem.set(f"members:{i[0]}")
            conn.commit()
            conn.close()

        def count_bok():
            conn = connect("Library.db")
            cu = conn.cursor()
            cu.execute("select count(*) from books")  # noqa
            result = cu.fetchall()
            for i in result:
                data_bok.set(f"books:{i[0]}")
            conn.commit()
            conn.close()

        def count_lon():
            conn = connect("Library.db")
            cu = conn.cursor()
            cu.execute("select count(*) from loans")  # noqa
            result = cu.fetchall()
            for i in result:
                data_lon.set(f"loans:{i[0]}")
            conn.commit()
            conn.close()

        def book_search(entry):
            conn = connect("Library.db")
            cu = conn.cursor()
            if not bol.get():
                cu.execute("select * from books where book_id = ?", (entry,))  # noqa
                result = cu.fetchall()
                if result:
                    for i in result:
                        rep_.set(
                            f"book number:{i[0]}\n title:{i[1]}\n product year:{i[2]}\n genre:{i[3]}\n avaiblecopies:{i[4]}\n wirter:{i[5]}")
                else:
                    rep_.set("book not found")
            if bol.get():
                cu.execute("select * from books where title = ?", (entry,))  # noqa
                result = cu.fetchall()
                if result:
                    for i in result:
                        rep_.set(
                            f"book number:{i[0]}\n title:{i[1]}\n product year:{i[2]}\n genre:{i[3]}\n avaiblecopies:{i[4]}\n wirter:{i[5]}")
                else:
                    rep_.set("book not found")
            conn.commit()
            conn.close()

        def member_search(entry):
            conn = connect("Library.db")
            cu = conn.cursor()
            if bol2.get():
                cu.execute("select * from members where name = ?", (entry,))  # noqa
                result = cu.fetchall()
                if result:
                    for i in result:
                        rep_.set(
                            f"member_id:{i[0]}\n fullname :{i[1]}\n address:{i[2]}\n phonenumber:{i[3]}\n joindate:{i[4]}\n age:{i[5]}\n loan:{i[6]}")
                else:
                    rep_.set("member not found")
            else:
                cu.execute("select * from members where member_id = ?", (entry,))  # noqa
                result = cu.fetchall()
                if result:
                    for i in result:
                        rep_.set(
                            f"member_id:{i[0]}\n fullname :{i[1]}\n address:{i[2]}\n phonenumber:{i[3]}\n joindate:{i[4]}\n age:{i[5]}\n loan:{i[6]}")
                else:
                    rep_.set("member not found")
            conn.commit()
            conn.close()

        label = Label(self, text="Library management system", font=("Tahoma", 30, "bold italic"), bg="#1F92DF", fg="white",
                      width=57,
                      height=2)
        label.place(x=0, y=0)

        label2 = Label(self, bg="#156DA8", fg="white", width=220, height=2)
        label2.place(x=0, y=90)

        loan_button = Button(self, text="loans", bg="#156DA8", fg="white", font=("mj_rajab regular", 13), width=10,
                             command=lambda: controller.show_frame(controller.page5))
        book_button = Button(self, text="books", bg="#156DA8", fg="white", font=("d", 13), width=10,
                             command=lambda: controller.show_frame(controller.page3))
        member_button = Button(self, text="members", bg="#156DA8", fg="white", font=("d", 13), width=10,
                               command=lambda: controller.show_frame(controller.page4))
        home_button = Button(self, text="home page", bg="#156DA8", fg="white", font=("d", 13), width=10,
                             command=lambda: controller.show_frame(controller.page2))
        book_button.place(x=560, y=90)
        member_button.place(x=670, y=90)
        home_button.place(x=780, y=90)
        loan_button.place(x=450, y=90)

        member_label = Label(self, textvariable=data_mem, justify="center", font=("d", 15, "bold italic"), height=6,
                             bg="#156DA8", fg="white",
                             width=14,
                             relief="raised")
        loan_label = Label(self, textvariable=data_lon, justify="center", font=("d", 15, "bold italic"), height=6,
                           bg="#156DA8", fg="white",
                           width=14,
                           relief="raised")
        book_label = Label(self, textvariable=data_bok, justify="center", font=("d", 15, "bold italic"), height=6,
                           bg="#156DA8", fg="white",
                           width=14, relief="raised")
        member_label.place(x=1100, y=143)
        loan_label.place(x=1100, y=263)
        book_label.place(x=1100, y=403)
        search_e = Entry(self, font=("s", 14), width=55)
        search_e.place(x=450, y=143)
        book_search_button = Button(self, text="book search", bg="#156DA8", fg="white", width=15,
                                    command=lambda: book_search(search_e.get()))
        member_search_button = Button(self, text="member search", bg="#156DA8", fg="white", width=15,
                                      command=lambda: member_search(search_e.get()))
        loan_search_button = Button(self, text="loan search", bg="#156DA8", fg="white", width=15,
                                    command=loan_search)
        book_search_button.place(x=0, y=143)
        member_search_button.place(x=130, y=143)
        loan_search_button.place(x=260, y=143)
        rep_label = Label(self, textvariable=rep_, height=12, width=67, bg="white", relief="raised",
                          font=("d", 20))
        rep_label.place(x=5, y=217)
        count_lon()
        count_bok()
        count_mem()
        title = Radiobutton(self, text="title", variable=bol, value=True, width=12, bg="silver", height=1)
        id = Radiobutton(self, text="id", variable=bol, value=False, width=12, bg="silver", height=1)
        name = Radiobutton(self, text="name", variable=bol2, value=True, bg="silver", width=10)
        id_member = Radiobutton(self, text="id", variable=bol2, value=False, bg="silver", width=10)
        title.place(x=0, y=173)
        id.place(x=0, y=193)
        name.place(x=130, y=173)
        id_member.place(x=130, y=193)


class Page3(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        data_ = StringVar()
        reset_1 = StringVar()
        reset_2 = StringVar()
        reset_3 = StringVar()
        reset_4 = StringVar()
        reset_5 = StringVar()
        reset_6 = StringVar()

        def mojavez():
            conn = connect("Library.db")
            cu = conn.cursor()
            cu.execute(
                "select * from books where book_id = ? AND title= ? AND birthday = ? AND genre = ? AND avablecopies = ? AND writer = ?",# noqa
                (answer_id2.get(), answer_t.get(), answer_pr.get(), answer_g.get(), answer_ac.get(), answer_w.get()))
            result = cu.fetchall()
            return not result

        def add_books(book_id_d, title_d, p_d, genre_d, ac_d, writer_d):
            lst = [(book_id_d, title_d, p_d, genre_d, ac_d, writer_d)]
            conn = connect("Library.db")
            cu = conn.cursor()

            if mojavez() and book_id_d != "" and title_d != "" and p_d != "" and genre_d != "" and ac_d != "" and writer_d != "":
                cu.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?)",  # noqa
                           (book_id_d, title_d, p_d, genre_d, ac_d, writer_d,))
                data_.set("Book added successfully.")
            else:
                data_.set("book can't add to library ")
            conn.commit()
            conn.close()

        def del_book():
            if answer_t.get() != "":
                conn = connect("library.db")
                cu = conn.cursor()
                cu.execute("delete from books where title = ?", (answer_t.get(),))  # noqa
                conn.commit()
                conn.close()
                data_.set("book deleted successfully")

            elif answer_id2 != "":
                conn = connect("library.db")
                cu = conn.cursor()
                cu.execute(f"delete from books where book_id = {answer_id2.get()}")  # noqa
                conn.commit()
                conn.close()
                data_.set("book deleted successfully")
            else:
                data_.set("we can't found this book delete book with title or book_id")

        def reset():
            answer_t.config(textvariable=reset_1)
            answer_id2.config(textvariable=reset_2)
            answer_pr.config(textvariable=reset_3)
            answer_g.config(textvariable=reset_4)
            answer_ac.config(textvariable=reset_5)
            answer_w.config(textvariable=reset_6)
            reset_1.set("")
            reset_2.set("")
            reset_3.set("")
            reset_4.set("")
            reset_5.set("")
            reset_6.set("")
            data_.set("")

        def edit_books(book_id_d, title_d, p_d, genre_d, ac_d, writer_d):
            conn = connect("library.db")
            cu = conn.cursor()

            update_fields = []
            values = []

            if title_d:
                update_fields.append("title = ?")
                values.append(title_d)
            if p_d:
                update_fields.append("sall_tolid = ?")
                values.append(p_d)
            if genre_d:
                update_fields.append("genre = ?")
                values.append(genre_d)
            if ac_d:
                update_fields.append("available_copies = ?")
                values.append(ac_d)
            if writer_d:
                update_fields.append("writer = ?")
                values.append(writer_d)

            values.append(book_id_d)

            if update_fields:
                update_query = f"UPDATE books SET {', '.join(update_fields)} WHERE book_id = ?"  # noqa

                try:
                    cu.execute(update_query, values)
                    conn.commit()
                    data_.set(f"Book ID {book_id_d} updated successfully.")
                except:
                    data_.set("error")
            else:
                data_.set("No fields to update.")

            conn.close()

        label = Label(self, text="Library management system", font=("l", 30, "bold italic"), bg="#1F92DF", fg="white",
                      width=57,
                      height=2)
        label.place(x=0, y=0)

        label2 = Label(self, bg="#156DA8", fg="white", width=220, height=2)
        label2.place(x=0, y=90)

        loan_button = Button(self, text="loans", bg="#156DA8", fg="white", font=("mj_rajab regular", 13), width=10,
                             command=lambda: controller.show_frame(controller.page5))
        book_button = Button(self, text="books", bg="#156DA8", fg="white", font=("d", 13), width=10,
                             command=lambda: controller.show_frame(controller.page3))
        member_button = Button(self, text="members", bg="#156DA8", fg="white", font=("d", 13), width=10,
                               command=lambda: controller.show_frame(controller.page4))
        home_button = Button(self, text="home page", bg="#156DA8", fg="white", font=("d", 13), width=10,
                             command=lambda: controller.show_frame(controller.page2))
        book_button.place(x=560, y=90)
        member_button.place(x=670, y=90)
        home_button.place(x=780, y=90)
        loan_button.place(x=450, y=90)
        book_id = Label(self, text="book id:", font=(10), fg="white", bg="gray", width=11)
        answer_id2 = Entry(self, width=60)
        book_title = Label(self, text="title:", font=(10), bg="gray", fg="white", width=11)
        answer_t = Entry(self, width=60)
        product_year = Label(self, text="product year", font=(10), fg="white", bg="gray", width=11)
        answer_pr = Entry(self, width=60)
        genre = Label(self, text="genre:", font=(10), bg="gray", fg="white", width=11)
        answer_g = Entry(self, width=60)
        avable_copies = Label(self, text="aviablcopies:", font=(10), bg="gray", fg="white", width=11)
        answer_ac = Entry(self, width=60)
        writer = Label(self, text="writer:", font=(10), bg="gray", fg="white", width=11)
        answer_w = Entry(self, width=60)
        book_id.place(x=50, y=200)
        book_title.place(x=50, y=250)
        product_year.place(x=50, y=300)
        genre.place(x=50, y=350)
        avable_copies.place(x=50, y=400)
        writer.place(x=50, y=450)
        answer_id2.place(x=180, y=200)
        answer_t.place(x=180, y=250)
        answer_pr.place(x=180, y=300)
        answer_g.place(x=180, y=350)
        answer_ac.place(x=180, y=400)
        answer_w.place(x=180, y=450)
        edit = Button(self, text="edit", bg="#156DA8", fg="white", width=10, height=7, font=("", 20),
                      command=lambda: edit_books(answer_id2.get(), answer_t.get(), answer_pr.get(), answer_g.get(),
                                                 answer_ac.get(), answer_w.get()))
        add = Button(self, text="add book", bg="#156DA8", fg="white", width=10, height=7, font=("", 20),
                     command=lambda: add_books(
                         answer_id2.get(),
                         answer_t.get(),
                         answer_pr.get(),
                         answer_g.get(),
                         answer_ac.get(),
                         answer_w.get()))
        delete = Button(self, text="delete book", bg="#156DA8", fg="white", width=10, height=7, font=("", 20),
                        command=del_book)
        reset_button = Button(self, text="clear away", bg="#156DA8", fg="white", width=35, height=1, font=("", 20),
                              command=reset)
        edit.place(x=680, y=200)
        add.place(x=880, y=200)
        delete.place(x=1080, y=200)
        reset_button.place(x=680, y=450)
        rep_view = Label(self, textvariable=data_, fg="red")
        rep_view.place(x=50, y=150)


class Page4(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        data_ = StringVar()
        reset_1 = StringVar()
        reset_2 = StringVar()
        reset_3 = StringVar()
        reset_4 = StringVar()
        reset_5 = StringVar()
        reset_6 = StringVar()
        reset_7 = StringVar()

        def reset():
            answer_id.config(textvariable=reset_1)
            answer_name.config(textvariable=reset_2)
            answer_p.config(textvariable=reset_3)
            answer_j.config(textvariable=reset_4)
            answer_loans.config(textvariable=reset_5)
            answer_a.config(textvariable=reset_6)
            answer_age.config(textvariable=reset_7)
            reset_1.set("")
            reset_2.set("")
            reset_3.set("")
            reset_4.set("")
            reset_5.set("")
            reset_6.set("")
            reset_7.set("")
            data_.set("")

        def mojavez():
            conn = connect("Library.db")
            cu = conn.cursor()
            cu.execute(
                "select * from members where member_id = ? AND name= ? AND address = ? AND phonenumber = ? AND join_date = ? AND age = ? AND loans = ?",# noqa
                (answer_id.get(), answer_name.get(), answer_a.get(), answer_p.get(), answer_j.get(), answer_age.get(),
                 answer_loans.get()))
            result = cu.fetchall()
            return not result

        def add_member():
            conn = connect("Library.db")
            cu = conn.cursor()

            if mojavez() and answer_id.get() != "" and answer_name.get() != "" and answer_loans.get() != "" and answer_a.get() != "" and answer_age.get() != "" and answer_j.get() != "" and answer_p.get() != "":
                cu.execute("INSERT INTO members VALUES (?, ?, ?, ?, ?, ?, ?)",  # noqa
                           (answer_id.get(), answer_name.get(), answer_a.get(), answer_p.get(), answer_j.get(),
                            answer_age.get(), answer_loans.get()))
                data_.set("member added successfully.")
            else:
                data_.set("member can't add to library ")
            conn.commit()
            conn.close()

        def del_member():
            if answer_name.get() != "":
                conn = connect("library.db")
                cu = conn.cursor()
                cu.execute("delete from members where name = ?", (answer_name.get(),))  # noqa
                data_.set("member deleted successfully")
                conn.commit()
                conn.close()

            elif answer_id != "":
                conn = connect("library.db")
                cu = conn.cursor()
                cu.execute(f"delete from members where member_id = {answer_id.get()}")  # noqa
                conn.commit()
                conn.close()
                data_.set("member deleted successfully")
            else:
                data_.set("we can't found this member delete member with name or member_id")

        def edit_members():
            conn = connect("library.db")
            cu = conn.cursor()

            update_fields = []
            values = []

            if answer_name.get():
                update_fields.append("name = ?")
                values.append(answer_name.get())
            if answer_a.get():
                update_fields.append("address = ?")
                values.append(answer_a.get())
            if answer_age.get():
                update_fields.append("age = ?")
                values.append(answer_age.get())
            if answer_loans.get():
                update_fields.append("loans = ?")
                values.append(answer_loans.get())
            if answer_j.get():
                update_fields.append("join_date = ?")
                values.append(answer_j.get())
            if answer_p.get():
                update_fields.append("phonenumber = ?")
                values.append(answer_p.get())
            values.append(answer_id.get())

            if update_fields:
                update_query = f"UPDATE members SET {', '.join(update_fields)} WHERE member_id = ?"  # noqa

                try:
                    cu.execute(update_query, values)
                    conn.commit()
                    data_.set(f"member ID {answer_id.get()} updated successfully.")
                except:
                    data_.set("error")
            else:
                data_.set("No fields to update.")

            conn.close()

        label = Label(self, text="Library management system", font=("l", 30, "bold italic"), bg="#1F92DF", fg="white",
                      width=57,
                      height=2)
        label.place(x=0, y=0)

        label2 = Label(self, bg="#156DA8", fg="white", width=220, height=2)
        label2.place(x=0, y=90)

        loan_button = Button(self, text="loans", bg="#156DA8", fg="white", font=("mj_rajab regular", 13), width=10,
                             command=lambda: controller.show_frame(controller.page5))
        book_button = Button(self, text="books", bg="#156DA8", fg="white", font=("d", 13), width=10,
                             command=lambda: controller.show_frame(controller.page3))
        member_button = Button(self, text="members", bg="#156DA8", fg="white", font=("d", 13), width=10,
                               command=lambda: controller.show_frame(controller.page4))
        home_button = Button(self, text="home page", bg="#156DA8", fg="white", font=("d", 13), width=10,
                             command=lambda: controller.show_frame(controller.page2))
        book_button.place(x=560, y=90)
        member_button.place(x=670, y=90)
        home_button.place(x=780, y=90)
        loan_button.place(x=450, y=90)
        member_id = Label(self, text="member id:", font=(10), bg="gray", fg="white", width=11)
        answer_id = Entry(self, width=60)
        name = Label(self, text="full name:", font=(10), bg="gray", fg="white", width=11)
        answer_name = Entry(self, width=60)
        address = Label(self, text="address:", font=(10), bg="gray", fg="white", width=11)
        answer_a = Entry(self, width=60)
        phonenumber = Label(self, text="phonenumber:", font=(10), bg="gray", fg="white", width=11)
        answer_p = Entry(self, width=60)
        join_date = Label(self, text="join date:", font=(10), bg="gray", fg="white", width=11)
        answer_j = Entry(self, width=60)
        age = Label(self, text="age:", font=(10), bg="gray", fg="white", width=11)
        answer_age = Entry(self, width=60)
        loans = Label(self, text="loans:", font=(10), bg="gray", fg="white", width=11)
        answer_loans = Entry(self, width=60)
        member_id.place(x=50, y=200)
        name.place(x=50, y=250)
        address.place(x=50, y=300)
        phonenumber.place(x=50, y=350)
        join_date.place(x=50, y=400)
        age.place(x=50, y=450)
        loans.place(x=50, y=500)
        answer_id.place(x=180, y=200)
        answer_name.place(x=180, y=250)
        answer_a.place(x=180, y=300)
        answer_p.place(x=180, y=350)
        answer_j.place(x=180, y=400)
        answer_age.place(x=180, y=450)
        answer_loans.place(x=180, y=500)
        edit = Button(self, text="edit", bg="#156DA8", fg="white", width=10, height=7, font=("", 20),
                      command=edit_members)
        add = Button(self, text="add member", bg="#156DA8", fg="white", width=10, height=7, font=("", 20),
                     command=add_member)
        delete = Button(self, text="delete member", bg="#156DA8", fg="white", width=10, height=7, font=("", 20),
                        command=del_member)
        reset_button = Button(self, text="پاک سازی", bg="#156DA8", fg="white", width=35, height=1, font=("", 20),
                              command=reset)
        edit.place(x=680, y=200)
        add.place(x=880, y=200)
        delete.place(x=1080, y=200)
        reset_button.place(x=680, y=450)
        rep_view = Label(self, textvariable=data_, fg="red")
        rep_view.place(x=50, y=150)


class Page5(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        data_ = StringVar()
        reset_1 = StringVar()
        reset_2 = StringVar()
        reset_3 = StringVar()
        reset_4 = StringVar()
        reset_5 = StringVar()

        def reset():
            answer_l.config(textvariable=reset_1)
            answer_bi.config(textvariable=reset_2)
            answer_mi.config(textvariable=reset_3)
            answer_ld.config(textvariable=reset_4)
            answer_rd.config(textvariable=reset_5)
            reset_1.set("")
            reset_2.set("")
            reset_3.set("")
            reset_4.set("")
            reset_5.set("")

            data_.set("")

        def mojavez():
            conn = connect("Library.db")
            cu = conn.cursor()
            cu.execute(
                "select * from loans where loan_id = ? AND book_id= ? AND member_id = ? AND loan_date = ? AND return_date = ? ",# noqa
                (answer_l.get(), answer_bi.get(), answer_mi.get(), answer_ld.get(), answer_rd.get()))
            result = cu.fetchall()
            return not result

        def add_loan():
            conn = connect("Library.db")
            cu = conn.cursor()

            if mojavez() and answer_l.get() != "" and answer_bi.get() != "" and answer_mi.get() != "" and answer_ld.get() != "" and answer_rd.get() != "":
                cu.execute("INSERT INTO members VALUES (?, ?, ?, ?, ?)",  # noqa
                           (answer_l.get(), answer_bi.get(), answer_mi.get(), answer_ld.get(), answer_rd.get()))
                data_.set("loan added successfully.")
            else:
                data_.set("loan can't add to library ")
            conn.commit()
            conn.close()

        def del_loan():

            conn = connect("library.db")
            cu = conn.cursor()
            try:
                cu.execute(f"delete from loans where loan_id = {answer_l.get()}")  # noqa
                conn.commit()
                data_.set("loan deleted successfully")
            except:
                data_.set("loan not exist")
            conn.close()

        def edit_loans():
            conn = connect("library.db")
            cu = conn.cursor()

            update_fields = []
            values = []

            if answer_bi.get():
                update_fields.append("book_id = ?")
                values.append(answer_bi.get())
            if answer_mi.get():
                update_fields.append("member_id = ?")
                values.append(answer_mi.get())
            if answer_ld.get():
                update_fields.append("loan_date = ?")
                values.append(answer_ld.get())
            if answer_rd.get():
                update_fields.append("return_date = ?")
                values.append(answer_rd.get())
            values.append(answer_l.get())

            if update_fields:
                update_query = f"UPDATE loans SET {', '.join(update_fields)} WHERE loan_id = ?"  # noqa

                try:
                    cu.execute(update_query, values)
                    conn.commit()
                    data_.set(f"loan ID {answer_l.get()} updated successfully.")
                except:
                    data_.set("error")
            else:
                data_.set("No fields to update.")

            conn.close()

        label = Label(self, text="Library management system", font=("l", 30, "bold italic"), bg="#1F92DF", fg="white",
                      width=57,
                      height=2)
        label.place(x=0, y=0)

        label2 = Label(self, bg="#156DA8", fg="white", width=220, height=2)
        label2.place(x=0, y=90)

        loan_button = Button(self, text="loans", bg="#156DA8", fg="white", font=("mj_rajab regular", 13)# noqa
                             , width=10,
                             # noqa
                             command=lambda: controller.show_frame(controller.page5))
        book_button = Button(self, text="books", bg="#156DA8", fg="white", font=("d", 13), width=10,  # noqa
                             command=lambda: controller.show_frame(controller.page3))
        member_button = Button(self, text="member", bg="#156DA8", fg="white", font=("d", 13), width=10,  # noqa
                               command=lambda: controller.show_frame(controller.page4))
        home_button = Button(self, text="home page", bg="#156DA8", fg="white", font=("d", 13), width=10,  # noqa
                             command=lambda: controller.show_frame(controller.page2))
        book_button.place(x=560, y=90)
        member_button.place(x=670, y=90)
        home_button.place(x=780, y=90)
        loan_button.place(x=450, y=90)

        loan_id = Label(self, text="loan id:", font=(10), bg="gray", fg="white", width=11)
        answer_l = Entry(self, width=60)
        book_id2 = Label(self, text="book id:", font=(10), bg="gray", fg="white", width=11)
        answer_bi = Entry(self, width=60)
        member_id2 = Label(self, text="member id:", font=(10), bg="gray", fg="white", width=11)
        answer_mi = Entry(self, width=60)
        loan_date = Label(self, text="loan date:", font=(10), bg="gray", fg="white", width=11)
        answer_ld = Entry(self, width=60)
        return_date = Label(self, text="return date:", font=(10), bg="gray", fg="white", width=11)
        answer_rd = Entry(self, width=60)
        loan_id.place(x=50, y=200)
        book_id2.place(x=50, y=250)
        member_id2.place(x=50, y=300)
        loan_date.place(x=50, y=350)
        return_date.place(x=50, y=400)
        answer_l.place(x=180, y=200)
        answer_bi.place(x=180, y=250)
        answer_mi.place(x=180, y=300)
        answer_ld.place(x=180, y=350)
        answer_rd.place(x=180, y=400)
        edit = Button(self, text="edit", bg="#156DA8", fg="white", width=10, height=7, font=("", 20),  # noqa
                      command=edit_loans)
        add = Button(self, text="add loan", bg="#156DA8", fg="white", width=10, height=7, font=("", 20),  # noqa
                     command=add_loan)
        delete = Button(self, text="delete loan", bg="#156DA8", fg="white", width=10, height=7, font=("", 20),  # noqa
                        command=del_loan)
        reset_button = Button(self, text="clear away", bg="#156DA8", fg="white", width=35, height=1, font=("", 20),
                              # noqa
                              command=reset)
        edit.place(x=680, y=200)
        add.place(x=880, y=200)
        delete.place(x=1080, y=200)
        reset_button.place(x=680, y=450)
        rep_view = Label(self, textvariable=data_, fg="red")
        rep_view.place(x=50, y=150)


root = Tk()
app = MultiPageApp(root)
root.mainloop()
