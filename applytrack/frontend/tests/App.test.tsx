import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../src/App";
import { request } from "../src/api";

vi.mock("../src/api", () => ({ request: vi.fn() }));
const mockedRequest = vi.mocked(request);

beforeEach(() => {
  localStorage.clear();
  mockedRequest.mockReset();
});

afterEach(() => vi.unstubAllGlobals());

describe("App", () => {
  it("registers an account and stores its access token", async () => {
    mockedRequest.mockResolvedValue([]);
    const fetchMock = vi.fn().mockResolvedValue(new Response('{"access_token":"new-token"}', { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    fireEvent.change(screen.getByPlaceholderText("Email"), { target: { value: "dev@example.com" } });
    fireEvent.change(screen.getByPlaceholderText("Password (8+ characters)"), { target: { value: "password123" } });
    fireEvent.click(screen.getByRole("button", { name: "Register" }));

    await waitFor(() => expect(localStorage.getItem("token")).toBe("new-token"));
    expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/auth/register", expect.objectContaining({ method: "POST" }));
    await waitFor(() => expect(mockedRequest).toHaveBeenCalledWith("/applications", "new-token"));
  });

  it("shows saved applications and signs out by clearing the token", async () => {
    localStorage.setItem("token", "existing-token");
    mockedRequest.mockResolvedValue([{ id: 1, company: "Example Co", role: "Engineer", status: "applied", notes: "" }]);
    render(<App />);

    expect(await screen.findByText("Engineer")).toBeInTheDocument();
    expect(screen.getByText("Example Co")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Sign out" }));

    expect(localStorage.getItem("token")).toBeNull();
    expect(screen.getByPlaceholderText("Email")).toBeInTheDocument();
  });
});
