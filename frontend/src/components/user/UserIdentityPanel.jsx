import { api } from "../../api/client";
import { useState } from "react";
import { v4 as uuidv4 } from "uuid";

export default function UserIdentityPanel({ onSessionReady }) {

  const [userId, setUserId] = useState("");
  const [sessionId, setSessionId] = useState("");

  const createUser = () => {

    const newUser = `user_${uuidv4().slice(0,6)}`;

    setUserId(newUser);

    setSessionId("");

  };

  const createSession = async () => {

    if (!userId) {
      alert("Create user first");
      return;
    }

    try {

      const newSession =
        `session_${uuidv4().slice(0,8)}`;

      setSessionId(newSession);

      await api.post(
        `/user/${userId}/session`,
        null,
        {
          params: {
            session_id: newSession
          }
        }
      );

      if (onSessionReady) {

        onSessionReady({
          userId: userId,
          sessionId: newSession
        });

      }

    }
    catch (err) {

      console.error(err);

      alert("Failed to register session");

    }

  };

  return (

    <div className="bg-gray-900 p-4 rounded-xl shadow-md mb-4">

      <h2 className="text-xl text-white mb-3">
        Identity Setup
      </h2>

      <div className="flex gap-2 mb-3">

        <button
          onClick={createUser}
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Create User
        </button>

        {userId && (

          <span className="text-green-400 text-sm">

            User:

            <span className="ml-2 font-mono">
              {userId}
            </span>

          </span>

        )}

      </div>

      <div className="flex gap-2">

        <button
          onClick={createSession}
          className="bg-green-600 px-4 py-2 rounded"
        >
          Create Session
        </button>

        {sessionId && (

          <span className="text-yellow-400 text-sm">

            Session:

            <span className="ml-2 font-mono">
              {sessionId}
            </span>

          </span>

        )}

      </div>

    </div>

  );

}