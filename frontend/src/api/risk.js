import { api } from "./client";

export const getRisk = async (entityType, entityId) => {
  const res = await api.get(
    `/correlation/risk/${entityType}/${entityId}`
  );
  return res.data;
};