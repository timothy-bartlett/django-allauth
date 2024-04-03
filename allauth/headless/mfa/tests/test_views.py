from allauth.account.models import EmailAddress, get_emailconfirmation_model


def test_auth_unverified_email_and_mfa(
    client,
    user_factory,
    password_factory,
    settings,
    totp_validation_bypass,
    headless_reverse,
    headless_client,
):
    settings.ACCOUNT_AUTHENTICATION_METHOD = "email"
    settings.ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    password = password_factory()
    user = user_factory(email_verified=False, password=password, with_totp=True)
    resp = client.post(
        headless_reverse("headless:login"),
        data={
            "email": user.email,
            "password": password,
        },
        content_type="application/json",
    )
    assert resp.status_code == 401
    # FIXME
    # assert resp.json() == {}
    emailaddress = EmailAddress.objects.filter(user=user, verified=False).get()
    key = get_emailconfirmation_model().create(emailaddress).key
    resp = client.post(
        headless_reverse("headless:verify_email"),
        data={"key": key},
        content_type="application/json",
    )
    assert resp.status_code == 401
    flows = [
        {
            "id": "login",
        },
        {
            "id": "signup",
        },
    ]
    if headless_client == "browser":
        flows.append(
            {
                "id": "provider_redirect",
                "providers": ["dummy", "openid_connect", "openid_connect"],
            }
        )
    flows.append(
        {
            "id": "mfa_authenticate",
            "is_pending": True,
        }
    )

    assert resp.json() == {
        "data": {"flows": flows},
        "meta": {"is_authenticated": False},
        "status": 401,
    }
    resp = client.post(
        headless_reverse("headless:mfa:authenticate"),
        data={"code": "bad"},
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert resp.json() == {
        "status": 400,
        "errors": [
            {"message": "Incorrect code.", "code": "incorrect_code", "param": "code"}
        ],
    }

    with totp_validation_bypass():
        resp = client.post(
            headless_reverse("headless:mfa:authenticate"),
            data={"code": "bad"},
            content_type="application/json",
        )
    assert resp.status_code == 200
