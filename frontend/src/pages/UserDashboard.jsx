import { useState } from "react";
import UserIdentityPanel from "../components/user/UserIdentityPanel";
import UserScanPanel from "../components/user/UserScanPanel";
import UserSessionHistory from "../components/user/UserSessionHistory";
import UserResultPanel from "../components/user/UserResultPanel";
import UserAdvicePanel from "../components/user/UserAdvicePanel";
import UserSessionSummary from "../components/user/UserSessionSummary";

export default function UserDashboard() {

  const [identity, setIdentity] = useState(null);

  const [selectedSession, setSelectedSession] = useState(null);

  return (

    <div className="min-h-screen bg-black text-white p-6">

      <h1 className="text-3xl font-bold mb-6">
        PHEMA User Portal
      </h1>

      <UserIdentityPanel
        onSessionReady={setIdentity}
      />

      {identity && (

        <>

          <UserScanPanel
            userId={identity.userId}
            sessionId={identity.sessionId}
          />

          <UserSessionHistory
            userId={identity.userId}
            onSelectSession={
              setSelectedSession
            }
          />

          {selectedSession && (

            <>

              <UserResultPanel
                userId={identity.userId}
                sessionId={selectedSession}
                entityId={selectedSession}
                entityType="session"
              />

              <UserSessionSummary
                userId={identity.userId}
                sessionId={selectedSession}
              />

              <UserAdvicePanel
                userId={identity.userId}
                sessionId={selectedSession}
              />

            </>

          )}
        </>

      )}

    </div>

  );

}