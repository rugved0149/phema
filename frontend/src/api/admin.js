import { api } from "./client";

export const getAnalytics = async () => {

  const res = await api.get(
    "/admin/analytics"
  );

  return res.data;

};