# src/index.js
# ============================================================
# Usage:
#   npx wrangler dev
#   npx wrangler deploy
# ============================================================

const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
};


function json(data, status = 200) {
    return new Response(JSON.stringify(data, null, 2), {
        status,
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            ...corsHeaders
        }
    });
}


async function createRequest(request, env) {
    const body = await request.json();

    const id = body.id;
    const purpose = body.purpose;
    const command = body.command;

    await env.DB.prepare(
        "INSERT INTO requests (id, status, purpose, command) VALUES (?, ?, ?, ?)"
    ).bind(
        id,
        "承認待ち",
        purpose,
        command
    ).run();

    return json({
        id: id,
        status: "承認待ち",
        purpose: purpose,
        command: command
    }, 201);
}


async function getRequest(id, env) {
    const result = await env.DB.prepare(
        "SELECT id, status, purpose, command, created_at, updated_at FROM requests WHERE id = ?"
    ).bind(id).first();

    if (!result) {
        return json({
            error: "指定されたIDは存在しません"
        }, 404);
    }

    return json(result);
}


async function getRequests(env) {
    const result = await env.DB.prepare(
        "SELECT id, status, purpose, command, created_at, updated_at FROM requests ORDER BY created_at DESC"
    ).all();

    return json(result.results);
}


async function approveRequest(id, env) {
    const result = await env.DB.prepare(
        "UPDATE requests SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    ).bind(
        "承認済み",
        id
    ).run();

    if (result.meta.changes === 0) {
        return json({
            error: "指定されたIDは存在しません"
        }, 404);
    }

    return getRequest(id, env);
}


export default {
    async fetch(request, env) {
        if (request.method === "OPTIONS") {
            return new Response(null, {
                headers: corsHeaders
            });
        }

        const url = new URL(request.url);
        const path = url.pathname;

        if (request.method === "POST" && path === "/api/requests") {
            return createRequest(request, env);
        }

        if (request.method === "GET" && path === "/api/requests") {
            return getRequests(env);
        }

        if (request.method === "GET" && path.startsWith("/api/requests/")) {
            const id = decodeURIComponent(path.split("/")[3]);
            return getRequest(id, env);
        }

        if (request.method === "POST" && path.startsWith("/api/requests/") && path.endsWith("/approve")) {
            const id = decodeURIComponent(path.split("/")[3]);
            return approveRequest(id, env);
        }

        return json({
            error: "Not Found"
        }, 404);
    }
};
