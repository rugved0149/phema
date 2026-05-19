import client from "./client";

export async function registerUser(
  email,
  username,
  password
) {

  return client.post(
    "/auth/register",
    null,
    {
      params: {
        email,
        username,
        password
      }
    }
  );
}

export async function verifyOTP(
  email,
  username,
  password,
  otp
) {

  return client.post(
    "/auth/verify",
    null,
    {
      params: {
        email,
        username,
        password,
        otp
      }
    }
  );
}

export async function loginUser(
  username,
  password
) {

  const res = await client.post(
    "/auth/login",
    null,
    {
      params: {
        username,
        password
      }
    }
  );

  /* STORE TOKENS */

  const access =
    res.data.access_token;

  const refresh =
    res.data.refresh_token;

  if (access) {

    localStorage.setItem(
      "token",
      access
    );

  }

  if (refresh) {

    localStorage.setItem(
      "refresh",
      refresh
    );

  }

  return res;

}