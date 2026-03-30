import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";

export default function UserResultPanel({
  userId,
  sessionId,
  entityId,
  entityType
}) {

  const { data } = useQuery({

    queryKey: [
      "risk",
      userId,
      sessionId,
      entityId
    ],

    queryFn: async () => {

      const res = await api.get(
        `/correlation/risk/${userId}/${sessionId}/${entityType}/${entityId}`
      );

      return res.data;

    },

    enabled:
      !!userId &&
      !!sessionId &&
      !!entityId,

    refetchInterval: 3000

  });


  const downloadReport = async () => {

    try {

      const response = await api.get(
        `/report/${userId}/${sessionId}`
      );

      const data = response.data;

      const blob = new Blob(
        [JSON.stringify(data, null, 2)],
        { type: "application/json" }
      );

      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;
      a.download = `${sessionId}_report.json`;

      document.body.appendChild(a);
      a.click();
      a.remove();

    } catch (err) {

      console.error(
        "Report download failed:",
        err
      );

    }

  };

  if (!data) return null;


  return (

    <div className="bg-gray-900 p-4 rounded-xl mt-4">

      <h2 className="text-xl text-white mb-3">
        Scan Results
      </h2>

      <div className="text-gray-300">

        Risk Score:
        <span className="ml-2 font-bold text-white">
          {data.risk_score}
        </span>

      </div>

      <div className="text-gray-300">

        Risk Level:
        <span className="ml-2 font-bold text-yellow-400">
          {data.risk_level}
        </span>

      </div>


      {/* DOWNLOAD BUTTON — NOW VISIBLE */}

      <div className="mt-4">

        <button
          onClick={downloadReport}
          className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded"
        >
          Download Report
        </button>

      </div>

    </div>

  );

}