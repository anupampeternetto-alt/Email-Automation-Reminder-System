
"use client";

import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8002";

export default function Home() {
  const [contacts, setContacts] = useState([]);
  const [reminders, setReminders] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const [contactsResponse, remindersResponse] =
          await Promise.all([
            fetch(`${API}/contacts/`),
            fetch(`${API}/reminders/`),
          ]);

        if (!contactsResponse.ok || !remindersResponse.ok) {
          throw new Error("API request failed");
        }

        setContacts(await contactsResponse.json());
        setReminders(await remindersResponse.json());
      } catch {
        setError("Cannot connect to FastAPI backend.");
      }
    }

    loadData();
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 p-10 text-white">
      <h1 className="mb-4 text-4xl font-bold">
        Email Automation & Reminder System
      </h1>

      <p className="mb-8 text-green-400">
        Automation Dashboard
      </p>

      {error && (
        <p className="mb-6 text-red-400">{error}</p>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-xl bg-slate-800 p-8">
          <h2 className="text-2xl font-semibold">
            Total Contacts
          </h2>
          <p className="mt-4 text-5xl font-bold">
            {contacts.length}
          </p>
        </div>

        <div className="rounded-xl bg-slate-800 p-8">
          <h2 className="text-2xl font-semibold">
            Total Reminders
          </h2>
          <p className="mt-4 text-5xl font-bold">
            {reminders.length}
          </p>
        </div>
      </div>
    </main>
  );
}
