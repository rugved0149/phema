import { api } from "./client";

export const getLiveEvents = async () => {
  const res = await api.get("/correlation/live");
  return res.data;
};