class CaptchaRepository:
    CREATE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS subscription_captcha (id_form GUID, captcha TEXT, expired INTEGER)"
    INSERT_SQL = "INSERT INTO subscription_captcha (id_form, captcha, expired) VALUES (?, ?, 0)"
    CHECK_SQL = "SELECT rowid FROM subscription_captcha WHERE id_form = ? AND captcha = ? AND expired = 0"
    UPDATE_SQL = "UPDATE subscription_captcha SET expired = 1 WHERE id_form = ?"

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_table(self):
        """Creates subscription_captcha table
        """
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(self.CREATE_TABLE_SQL)
            self.db_connection.commit()
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()

    def check(self, id_form, captcha):
        """Check for existing row by the given form ID and captcha code.

        :param id_form: form ID
        :param captcha: captcha code
        """
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            data = cursor.execute(self.CHECK_SQL, (id_form, captcha))
            return data.fetchone()
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()

    def create_form(self, id_form, captcha):
        """Insert a new form with its generated captcha code.

        :param id_form: form ID
        :param captcha: captcha code
        """
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            cursor.executemany(self.INSERT_SQL, [(id_form, captcha)])
            self.db_connection.commit()
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()

    def update_form(self, id_form):
        """Update an existing form setting expired flag.

        :param id_form: form ID
        """
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(self.UPDATE_SQL, (id_form,))
            self.db_connection.commit()
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
