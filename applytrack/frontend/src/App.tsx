import { useEffect, useState } from "react";
import { request } from "./api";
type Item = { id:number; company:string; role:string; status:string; notes:string };
const statuses = ["saved","applied","interview","offer","rejected"];
export function App() {
  const [token,setToken] = useState(localStorage.getItem("token") ?? "");
  const [email,setEmail] = useState(""); const [password,setPassword] = useState("");
  const [items,setItems] = useState<Item[]>([]); const [error,setError] = useState("");
  const [company,setCompany] = useState(""); const [role,setRole] = useState("");
  async function auth(path:string) {
    try { const body = path.endsWith("login") ? new URLSearchParams({username:email,password}) : JSON.stringify({email,password});
      const r = await fetch(`http://localhost:8000${path}`, {method:"POST",headers:{"Content-Type":path.endsWith("login")?"application/x-www-form-urlencoded":"application/json"},body});
      if(!r.ok) throw new Error((await r.json()).detail); const data=await r.json(); const t=data.access_token;
      setToken(t); localStorage.setItem("token",t); setError("");
    } catch(e) { setError(String(e)); }
  }
  async function refresh() { try { setItems(await request("/applications",token)); setError(""); } catch(e) { setError(String(e)); } }
  useEffect(()=>{ if(token) void refresh(); },[token]);
  async function add(e:React.FormEvent) { e.preventDefault(); try { await request("/applications",token,{method:"POST",body:JSON.stringify({company,role})}); setCompany("");setRole("");await refresh(); } catch(e){setError(String(e));} }
  async function change(item:Item,status:string) { await request(`/applications/${item.id}`,token,{method:"PATCH",body:JSON.stringify({status})}); await refresh(); }
  async function remove(id:number) { await request(`/applications/${id}`,token,{method:"DELETE"}); await refresh(); }
  if(!token) return <main><h1>ApplyTrack</h1><p>Keep your job search organized.</p><section><input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)}/><input placeholder="Password (8+ characters)" type="password" value={password} onChange={e=>setPassword(e.target.value)}/><button onClick={()=>auth("/auth/register")}>Register</button><button onClick={()=>auth("/auth/login")}>Login</button></section>{error}</main>;
  return <main><header><div><h1>ApplyTrack</h1><p>Your job search, in one place.</p></div><button onClick={()=>{localStorage.removeItem("token");setToken("");}}>Sign out</button></header>
    <form onSubmit={add}><input required placeholder="Company" value={company} onChange={e=>setCompany(e.target.value)}/><input required placeholder="Role" value={role} onChange={e=>setRole(e.target.value)}/><button>Add application</button></form>
    <h2>Applications ({items.length})</h2><div className="grid">{items.map(item=><article key={item.id}><h3>{item.role}</h3><p>{item.company}</p><select value={item.status} onChange={e=>change(item,e.target.value)}>{statuses.map(s=><option key={s}>{s}</option>)}</select><button onClick={()=>remove(item.id)}>Delete</button></article>)}</div>{error&&<p role="alert">{error}</p>}
  </main>;
}
