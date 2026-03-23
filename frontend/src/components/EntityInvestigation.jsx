import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getRisk } from "../api/risk";

export default function EntityInvestigation() {

  const [entityId, setEntityId] = useState("");
  const [entityType, setEntityType] = useState("session");

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["risk", entityType, entityId],
    queryFn: () => getRisk(entityType, entityId),
    enabled: false
  });

  const handleSearch = () => {
    if (!entityId) return;
    refetch();
  };

  return (
    <div className="bg-gray-900 p-4 rounded-xl shadow-md">

      <h2 className="text-xl font-semibold mb-4 text-white">
        Entity Investigation
      </h2>

      {/* Input Section */}

      <div className="flex gap-2 mb-4">

        <select
          value={entityType}
          onChange={(e) =>
            setEntityType(e.target.value)
          }
          className="bg-gray-800 text-white px-2 py-1 rounded"
        >

          <option value="session">Session</option>
          <option value="user">User</option>
          <option value="ip">IP</option>
          <option value="file">File</option>

        </select>

        <input
          type="text"
          placeholder="Enter entity ID"
          value={entityId}
          onChange={(e) =>
            setEntityId(e.target.value)
          }
          className="flex-1 bg-gray-800 text-white px-3 py-1 rounded"
        />

        <button
          onClick={handleSearch}
          className="bg-blue-600 px-4 py-1 rounded hover:bg-blue-700"
        >
          Analyze
        </button>

      </div>

      {/* Loading */}

      {isLoading && (
        <div className="text-gray-400">
          Analyzing...
        </div>
      )}

      {/* Error */}

      {error && (
        <div className="text-red-500">
          Failed to fetch risk data
        </div>
      )}

      {/* Output */}

      {data && (

        <div className="space-y-4">

          {/* Risk Score */}

          <div>
            <span className="text-gray-400">
              Risk Score:
            </span>

            <span className="text-white font-bold ml-2">
              {data.risk_score}
            </span>
          </div>

          {/* Risk Level */}

          <div>
            <span className="text-gray-400">
              Risk Level:
            </span>

            <span
              className={`font-bold ml-2 ${
                data.risk_level === "HIGH"
                  ? "text-red-500"
                  : data.risk_level === "MEDIUM"
                  ? "text-yellow-400"
                  : "text-green-400"
              }`}
            >
              {data.risk_level}
            </span>
          </div>

          {/* Attack Type */}

          {data.attack_type && (

            <div>
              <span className="text-gray-400">
                Attack Type:
              </span>

              <span className="text-purple-400 font-bold ml-2">
                {data.attack_type}
              </span>
            </div>

          )}

          {/* MITRE Techniques */}

          {data.mitre_attack &&
            data.mitre_attack.length > 0 && (

            <div>

              <span className="text-gray-400">
                MITRE Techniques:
              </span>

              <div className="flex flex-wrap gap-2 mt-2">

                {data.mitre_attack.map((t, i) => (

                  <span
                    key={i}
                    className="bg-red-600 px-2 py-1 text-xs rounded"
                  >
                    {t.id}
                  </span>

                ))}

              </div>

            </div>

          )}

          {/* Score Breakdown */}

          {data.breakdown && (

            <div>

              <span className="text-gray-400">
                Score Breakdown:
              </span>

              <ul className="list-disc ml-5 mt-1 text-sm text-gray-300">

                {Object.entries(data.breakdown)
                  .map(([key, value]) => (

                    <li key={key}>
                      {key}: {value}
                    </li>

                  ))}

              </ul>

            </div>

          )}

          {/* Reasons */}

          {data.reasons && (

            <div>

              <span className="text-gray-400">
                Reasons:
              </span>

              <ul className="list-disc ml-5 mt-1 text-sm text-gray-300">

                {data.reasons.map((r, i) => (

                  <li key={i}>
                    {r}
                  </li>

                ))}

              </ul>

            </div>

          )}

        </div>

      )}

    </div>
  );
}