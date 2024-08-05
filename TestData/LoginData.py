import pytest


@pytest.mark.usefixtures("base_url")
class TestLoginData:
    def test_get_user_data(self,base_url):
        if base_url == "demo":
            return {"mail": "feteb17715@randrai.com", "password": "Okoora1!","user_id":"defddb4a-a050-4afd-bebc-2bb7cfd7a6a3","url": "https://demo2.okoora.com/login/"}
        else:
            return {"mail": "jipop81748@in2reach.com", "password": "Okoora2!","url":"https://okoora-qa-front2023.azurewebsites.net/login","user_id":"a11103d7-51c3-458a-ae24-775858544a97"}
    # EUDemoLoginData = [{"mail": "sevafag866@hisotyr.com", "password": "Xt%2Fn&7"}]
    # LoginQA=[{"mail":"jipop81748@in2reach.com","password":"Okoora2!"}]
    # qa_url = {"https://okoora-qa-front2023.azurewebsites.net/login"}
        login_role_user = {"manager_mail":"tiwoti5085@meogl.com","manager_password":"Okoora1!"}

