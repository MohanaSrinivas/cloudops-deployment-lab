import { afterEach, describe, expect, it, vi } from "vitest";
import { request } from "../src/api";

afterEach(() => vi.unstubAllGlobals());

describe("request", () => {
  it("sends the bearer token and returns JSON", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response('{"id":7}', { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    await expect(request("/applications", "session-token")).resolves.toEqual({ id: 7 });
    expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/applications", {
      headers: { "Content-Type": "application/json", Authorization: "Bearer session-token" },
    });
  });

  it("returns null for a successful no-content response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(null, { status: 204 })));

    await expect(request("/applications/7", "session-token", { method: "DELETE" })).resolves.toBeNull();
  });

  it("surfaces API error details", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response('{"detail":"Unauthorized"}', { status: 401 })));

    await expect(request("/applications", "expired-token")).rejects.toThrow("Unauthorized");
  });
});
