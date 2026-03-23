import { api } from "./client";

export const getSystemStatus = async () => {
    const res = await api.get("/system/status");
    return res.data;
};