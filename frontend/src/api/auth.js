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

  return client.post(
    "/auth/login",
    null,
    {
      params: {
        username,
        password
      }
    }
  );
}