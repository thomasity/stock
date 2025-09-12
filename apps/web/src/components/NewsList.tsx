"use client";
import { useState } from "react";

type Article = {
    id: string;
    title: string;
    url: string;
    source: string;
    published_at: string;
    tickers?: string[];
};

const PAGE_SIZE = 6;

export default function NewsList({ items }: { items: Article[] }) {
    const [page, setPage] = useState(0);
    const totalPages = Math.ceil((items?.length ?? 0) / PAGE_SIZE);

    const pagedItems = items?.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE) ?? [];

    return (
        <div className="theme-container overflow-auto">
            <div className="px-4 py-3 border-b">
                <h2 className="text-lg font-medium">Latest News</h2>
            </div>
            <ul className="divide-y">
                {pagedItems.length ? pagedItems.map((a) => (
                    <li
                        key={a.id}
                        className="p-4 flex flex-col justify-between h-32" // fixed height, flex layout
                        style={{ minHeight: "8rem" }} // fallback for h-32
                    >
                        <a className="font-medium hover:underline" href={a.url} target="_blank" rel="noreferrer">
                            {a.title}
                        </a>
                        <div className="text-xs text-gray-500 mt-1">
                            {a.source} · {new Date(a.published_at).toLocaleString()} · {(a.tickers ?? []).join(", ")}
                        </div>
                    </li>
                )) : (
                    <li className="p-4 text-gray-500 h-32 flex items-center justify-center" style={{ minHeight: "8rem" }}>
                        No news yet
                    </li>
                )}
            </ul>
            {totalPages > 1 && (
                <div className="flex justify-center items-center gap-2 py-2 border-t">
                    <button
                        className="align-middle px-2 py-1 rounded bg-gray-100 hover:bg-gray-200 disabled:opacity-50"
                        onClick={() => setPage((p) => Math.max(0, p - 1))}
                        disabled={page === 0}
                        aria-label="Previous page"
                    >
                        ←
                    </button>
                    <span className="text-sm text-gray-600">
                        Page {page + 1} of {totalPages}
                    </span>
                    <button
                        className="px-2 py-1 rounded bg-gray-100 hover:bg-gray-200 disabled:opacity-50"
                        onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                        disabled={page >= totalPages - 1}
                        aria-label="Next page"
                    >
                        →
                    </button>
                </div>
            )}
        </div>
    );
}
