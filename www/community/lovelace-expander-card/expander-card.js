var fi = Object.defineProperty;
var Qn = (e) => {
  throw TypeError(e);
};
var ui = (e, t, n) => t in e ? fi(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var M = (e, t, n) => ui(e, typeof t != "symbol" ? t + "" : t, n), yn = (e, t, n) => t.has(e) || Qn("Cannot " + n);
var u = (e, t, n) => (yn(e, t, "read from private field"), n ? n.call(e) : t.get(e)), C = (e, t, n) => t.has(e) ? Qn("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, n), m = (e, t, n, i) => (yn(e, t, "write to private field"), i ? i.call(e, n) : t.set(e, n), n), j = (e, t, n) => (yn(e, t, "access private method"), n);
var ur;
typeof window < "u" && ((ur = window.__svelte ?? (window.__svelte = {})).v ?? (ur.v = /* @__PURE__ */ new Set())).add("5");
const ci = 1, di = 2, hi = 16, vi = 1, pi = 2, cr = "[", fn = "[!", In = "]", St = {}, Y = Symbol(), _i = "http://www.w3.org/1999/xhtml", gi = "http://www.w3.org/2000/svg", dr = !1;
var Pn = Array.isArray, mi = Array.prototype.indexOf, zn = Array.from, Zt = Object.keys, Ct = Object.defineProperty, wt = Object.getOwnPropertyDescriptor, wi = Object.getOwnPropertyDescriptors, yi = Object.prototype, bi = Array.prototype, hr = Object.getPrototypeOf, er = Object.isExtensible;
function $i(e) {
  for (var t = 0; t < e.length; t++)
    e[t]();
}
function vr() {
  var e, t, n = new Promise((i, r) => {
    e = i, t = r;
  });
  return { promise: n, resolve: e, reject: t };
}
const H = 2, Dn = 4, Ln = 8, ht = 16, Fe = 32, Ze = 64, un = 128, X = 1024, ne = 2048, Qe = 4096, fe = 8192, De = 16384, Fn = 32768, Bt = 65536, tr = 1 << 17, Ei = 1 << 18, vt = 1 << 19, xi = 1 << 20, _e = 256, Qt = 512, en = 32768, $n = 1 << 21, Bn = 1 << 22, ot = 1 << 23, Ut = Symbol("$state"), ki = Symbol("legacy props"), Ti = Symbol(""), mt = new class extends Error {
  constructor() {
    super(...arguments);
    M(this, "name", "StaleReactionError");
    M(this, "message", "The reaction that called `getAbortSignal()` was re-run or destroyed");
  }
}(), Si = 1, Yn = 3, Nt = 8;
function Ci(e) {
  throw new Error("https://svelte.dev/e/lifecycle_outside_component");
}
function qi() {
  throw new Error("https://svelte.dev/e/async_derived_orphan");
}
function Ai(e) {
  throw new Error("https://svelte.dev/e/effect_in_teardown");
}
function Oi() {
  throw new Error("https://svelte.dev/e/effect_in_unowned_derived");
}
function Ni(e) {
  throw new Error("https://svelte.dev/e/effect_orphan");
}
function Ri() {
  throw new Error("https://svelte.dev/e/effect_update_depth_exceeded");
}
function ji() {
  throw new Error("https://svelte.dev/e/hydration_failed");
}
function Mi() {
  throw new Error("https://svelte.dev/e/state_descriptors_fixed");
}
function Ii() {
  throw new Error("https://svelte.dev/e/state_prototype_fixed");
}
function Pi() {
  throw new Error("https://svelte.dev/e/state_unsafe_mutation");
}
function zi() {
  throw new Error("https://svelte.dev/e/svelte_boundary_reset_onerror");
}
function cn(e) {
  console.warn("https://svelte.dev/e/hydration_mismatch");
}
function Di() {
  console.warn("https://svelte.dev/e/svelte_boundary_reset_noop");
}
let y = !1;
function K(e) {
  y = e;
}
let x;
function P(e) {
  if (e === null)
    throw cn(), St;
  return x = e;
}
function qt() {
  return P(
    /** @type {TemplateNode} */
    /* @__PURE__ */ Re(x)
  );
}
function Me(e) {
  if (y) {
    if (/* @__PURE__ */ Re(x) !== null)
      throw cn(), St;
    x = e;
  }
}
function Li(e = 1) {
  if (y) {
    for (var t = e, n = x; t--; )
      n = /** @type {TemplateNode} */
      /* @__PURE__ */ Re(n);
    x = n;
  }
}
function tn(e = !0) {
  for (var t = 0, n = x; ; ) {
    if (n.nodeType === Nt) {
      var i = (
        /** @type {Comment} */
        n.data
      );
      if (i === In) {
        if (t === 0) return n;
        t -= 1;
      } else (i === cr || i === fn) && (t += 1);
    }
    var r = (
      /** @type {TemplateNode} */
      /* @__PURE__ */ Re(n)
    );
    e && n.remove(), n = r;
  }
}
function pr(e) {
  if (!e || e.nodeType !== Nt)
    throw cn(), St;
  return (
    /** @type {Comment} */
    e.data
  );
}
function _r(e) {
  return e === this.v;
}
function Fi(e, t) {
  return e != e ? t == t : e !== t || e !== null && typeof e == "object" || typeof e == "function";
}
function gr(e) {
  return !Fi(e, this.v);
}
let Bi = !1, ue = null;
function At(e) {
  ue = e;
}
function Vn(e, t = !1, n) {
  ue = {
    p: ue,
    c: null,
    e: null,
    s: e,
    x: null,
    l: null
  };
}
function Hn(e) {
  var t = (
    /** @type {ComponentContext} */
    ue
  ), n = t.e;
  if (n !== null) {
    t.e = null;
    for (var i of n)
      Dr(i);
  }
  return e !== void 0 && (t.x = e), ue = t.p, e ?? /** @type {T} */
  {};
}
function mr() {
  return !0;
}
let rt = [];
function wr() {
  var e = rt;
  rt = [], $i(e);
}
function dn(e) {
  if (rt.length === 0 && !Mt) {
    var t = rt;
    queueMicrotask(() => {
      t === rt && wr();
    });
  }
  rt.push(e);
}
function Yi() {
  for (; rt.length > 0; )
    wr();
}
const Vi = /* @__PURE__ */ new WeakMap();
function yr(e) {
  var t = k;
  if (t === null)
    return E.f |= ot, e;
  if ((t.f & Fn) === 0) {
    if ((t.f & un) === 0)
      throw !t.parent && e instanceof Error && br(e), e;
    t.b.error(e);
  } else
    Ot(e, t);
}
function Ot(e, t) {
  for (; t !== null; ) {
    if ((t.f & un) !== 0)
      try {
        t.b.error(e);
        return;
      } catch (n) {
        e = n;
      }
    t = t.parent;
  }
  throw e instanceof Error && br(e), e;
}
function br(e) {
  const t = Vi.get(e);
  t && (Ct(e, "message", {
    value: t.message
  }), Ct(e, "stack", {
    value: t.stack
  }));
}
const Yt = /* @__PURE__ */ new Set();
let R = null, D = null, En = /* @__PURE__ */ new Set(), Ne = [], hn = null, xn = !1, Mt = !1;
var $t, Et, xt, it, zt, kt, Tt, L, kn, nt, Tn, $r;
const an = class an {
  constructor() {
    C(this, L);
    M(this, "committed", !1);
    /**
     * The current values of any sources that are updated in this batch
     * They keys of this map are identical to `this.#previous`
     * @type {Map<Source, any>}
     */
    M(this, "current", /* @__PURE__ */ new Map());
    /**
     * The values of any sources that are updated in this batch _before_ those updates took place.
     * They keys of this map are identical to `this.#current`
     * @type {Map<Source, any>}
     */
    C(this, $t, /* @__PURE__ */ new Map());
    /**
     * When the batch is committed (and the DOM is updated), we need to remove old branches
     * and append new ones by calling the functions added inside (if/each/key/etc) blocks
     * @type {Set<() => void>}
     */
    C(this, Et, /* @__PURE__ */ new Set());
    /**
     * The number of async effects that are currently in flight
     */
    C(this, xt, 0);
    /**
     * The number of async effects that are currently in flight, _not_ inside a pending boundary
     */
    C(this, it, 0);
    /**
     * A deferred that resolves when the batch is committed, used with `settled()`
     * TODO replace with Promise.withResolvers once supported widely enough
     * @type {{ promise: Promise<void>, resolve: (value?: any) => void, reject: (reason: unknown) => void } | null}
     */
    C(this, zt, null);
    /**
     * Deferred effects (which run after async work has completed) that are DIRTY
     * @type {Effect[]}
     */
    C(this, kt, []);
    /**
     * Deferred effects that are MAYBE_DIRTY
     * @type {Effect[]}
     */
    C(this, Tt, []);
    /**
     * A set of branches that still exist, but will be destroyed when this batch
     * is committed — we skip over these during `process`
     * @type {Set<Effect>}
     */
    M(this, "skipped_effects", /* @__PURE__ */ new Set());
  }
  /**
   *
   * @param {Effect[]} root_effects
   */
  process(t) {
    Ne = [], this.apply();
    var n = {
      parent: null,
      effect: null,
      effects: [],
      render_effects: [],
      block_effects: []
    };
    for (const i of t)
      j(this, L, kn).call(this, i, n);
    j(this, L, Tn).call(this), u(this, it) > 0 ? (j(this, L, nt).call(this, n.effects), j(this, L, nt).call(this, n.render_effects), j(this, L, nt).call(this, n.block_effects)) : (R = null, nr(n.render_effects), nr(n.effects)), D = null;
  }
  /**
   * Associate a change to a given source with the current
   * batch, noting its previous and current values
   * @param {Source} source
   * @param {any} value
   */
  capture(t, n) {
    u(this, $t).has(t) || u(this, $t).set(t, n), this.current.set(t, t.v), D == null || D.set(t, t.v);
  }
  activate() {
    R = this;
  }
  deactivate() {
    R = null, D = null;
  }
  flush() {
    if (Ne.length > 0) {
      if (this.activate(), Er(), R !== null && R !== this)
        return;
    } else
      j(this, L, Tn).call(this);
    this.deactivate();
    for (const t of En)
      if (En.delete(t), t(), R !== null)
        break;
  }
  /**
   *
   * @param {boolean} blocking
   */
  increment(t) {
    m(this, xt, u(this, xt) + 1), t && m(this, it, u(this, it) + 1);
  }
  /**
   *
   * @param {boolean} blocking
   */
  decrement(t) {
    m(this, xt, u(this, xt) - 1), t && m(this, it, u(this, it) - 1);
    for (const n of u(this, kt))
      Z(n, ne), ct(n);
    for (const n of u(this, Tt))
      Z(n, Qe), ct(n);
    m(this, kt, []), m(this, Tt, []), this.flush();
  }
  /** @param {() => void} fn */
  add_callback(t) {
    u(this, Et).add(t);
  }
  settled() {
    return (u(this, zt) ?? m(this, zt, vr())).promise;
  }
  static ensure() {
    if (R === null) {
      const t = R = new an();
      Yt.add(R), Mt || an.enqueue(() => {
        R === t && t.flush();
      });
    }
    return R;
  }
  /** @param {() => void} task */
  static enqueue(t) {
    dn(t);
  }
  apply() {
  }
};
$t = new WeakMap(), Et = new WeakMap(), xt = new WeakMap(), it = new WeakMap(), zt = new WeakMap(), kt = new WeakMap(), Tt = new WeakMap(), L = new WeakSet(), /**
 * Traverse the effect tree, executing effects or stashing
 * them for later execution as appropriate
 * @param {Effect} root
 * @param {EffectTarget} target
 */
kn = function(t, n) {
  var c;
  t.f ^= X;
  for (var i = t.first; i !== null; ) {
    var r = i.f, s = (r & (Fe | Ze)) !== 0, a = s && (r & X) !== 0, l = a || (r & fe) !== 0 || this.skipped_effects.has(i);
    if ((i.f & un) !== 0 && ((c = i.b) != null && c.is_pending()) && (n = {
      parent: n,
      effect: i,
      effects: [],
      render_effects: [],
      block_effects: []
    }), !l && i.fn !== null) {
      s ? i.f ^= X : (r & Dn) !== 0 ? n.effects.push(i) : _n(i) && ((i.f & ht) !== 0 && n.block_effects.push(i), sn(i));
      var o = i.first;
      if (o !== null) {
        i = o;
        continue;
      }
    }
    var f = i.parent;
    for (i = i.next; i === null && f !== null; )
      f === n.effect && (j(this, L, nt).call(this, n.effects), j(this, L, nt).call(this, n.render_effects), j(this, L, nt).call(this, n.block_effects), n = /** @type {EffectTarget} */
      n.parent), i = f.next, f = f.parent;
  }
}, /**
 * @param {Effect[]} effects
 */
nt = function(t) {
  for (const n of t)
    ((n.f & ne) !== 0 ? u(this, kt) : u(this, Tt)).push(n), Z(n, X);
}, Tn = function() {
  if (u(this, it) === 0) {
    for (const t of u(this, Et)) t();
    u(this, Et).clear();
  }
  u(this, xt) === 0 && j(this, L, $r).call(this);
}, $r = function() {
  var r, s;
  if (Yt.size > 1) {
    u(this, $t).clear();
    var t = D, n = !0, i = {
      parent: null,
      effect: null,
      effects: [],
      render_effects: [],
      block_effects: []
    };
    for (const a of Yt) {
      if (a === this) {
        n = !1;
        continue;
      }
      const l = [];
      for (const [f, c] of this.current) {
        if (a.current.has(f))
          if (n && c !== a.current.get(f))
            a.current.set(f, c);
          else
            continue;
        l.push(f);
      }
      if (l.length === 0)
        continue;
      const o = [...a.current.keys()].filter((f) => !this.current.has(f));
      if (o.length > 0) {
        const f = /* @__PURE__ */ new Set(), c = /* @__PURE__ */ new Map();
        for (const v of l)
          xr(v, o, f, c);
        if (Ne.length > 0) {
          R = a, a.apply();
          for (const v of Ne)
            j(r = a, L, kn).call(r, v, i);
          Ne = [], a.deactivate();
        }
      }
    }
    R = null, D = t;
  }
  this.committed = !0, Yt.delete(this), (s = u(this, zt)) == null || s.resolve();
};
let Le = an;
function oe(e) {
  var t = Mt;
  Mt = !0;
  try {
    for (var n; ; ) {
      if (Yi(), Ne.length === 0 && (R == null || R.flush(), Ne.length === 0))
        return hn = null, /** @type {T} */
        n;
      Er();
    }
  } finally {
    Mt = t;
  }
}
function Er() {
  var e = bt;
  xn = !0;
  try {
    var t = 0;
    for (ir(!0); Ne.length > 0; ) {
      var n = Le.ensure();
      if (t++ > 1e3) {
        var i, r;
        Hi();
      }
      n.process(Ne), Ge.clear();
    }
  } finally {
    xn = !1, ir(e), hn = null;
  }
}
function Hi() {
  try {
    Ri();
  } catch (e) {
    Ot(e, hn);
  }
}
let ye = null;
function nr(e) {
  var t = e.length;
  if (t !== 0) {
    for (var n = 0; n < t; ) {
      var i = e[n++];
      if ((i.f & (De | fe)) === 0 && _n(i) && (ye = /* @__PURE__ */ new Set(), sn(i), i.deps === null && i.first === null && i.nodes_start === null && (i.teardown === null && i.ac === null ? Yr(i) : i.fn = null), (ye == null ? void 0 : ye.size) > 0)) {
        Ge.clear();
        for (const r of ye) {
          if ((r.f & (De | fe)) !== 0) continue;
          const s = [r];
          let a = r.parent;
          for (; a !== null; )
            ye.has(a) && (ye.delete(a), s.push(a)), a = a.parent;
          for (let l = s.length - 1; l >= 0; l--) {
            const o = s[l];
            (o.f & (De | fe)) === 0 && sn(o);
          }
        }
        ye.clear();
      }
    }
    ye = null;
  }
}
function xr(e, t, n, i) {
  if (!n.has(e) && (n.add(e), e.reactions !== null))
    for (const r of e.reactions) {
      const s = r.f;
      (s & H) !== 0 ? xr(
        /** @type {Derived} */
        r,
        t,
        n,
        i
      ) : (s & (Bn | ht)) !== 0 && (s & ne) === 0 && // we may have scheduled this one already
      kr(r, t, i) && (Z(r, ne), ct(
        /** @type {Effect} */
        r
      ));
    }
}
function kr(e, t, n) {
  const i = n.get(e);
  if (i !== void 0) return i;
  if (e.deps !== null)
    for (const r of e.deps) {
      if (t.includes(r))
        return !0;
      if ((r.f & H) !== 0 && kr(
        /** @type {Derived} */
        r,
        t,
        n
      ))
        return n.set(
          /** @type {Derived} */
          r,
          !0
        ), !0;
    }
  return n.set(e, !1), !1;
}
function ct(e) {
  for (var t = hn = e; t.parent !== null; ) {
    t = t.parent;
    var n = t.f;
    if (xn && t === k && (n & ht) !== 0)
      return;
    if ((n & (Ze | Fe)) !== 0) {
      if ((n & X) === 0) return;
      t.f ^= X;
    }
  }
  Ne.push(t);
}
function Ui(e) {
  let t = 0, n = dt(0), i;
  return () => {
    is() && (_(n), Wn(() => (t === 0 && (i = Gn(() => e(() => It(n)))), t += 1, () => {
      dn(() => {
        t -= 1, t === 0 && (i == null || i(), i = void 0, It(n));
      });
    })));
  };
}
var Wi = Bt | vt | un;
function Xi(e, t, n) {
  new Ki(e, t, n);
}
var $e, le, Dt, Ce, st, qe, he, te, Ae, Ue, at, We, lt, Xe, ln, on, F, Tr, Sr, Wt, Xt, Sn;
class Ki {
  /**
   * @param {TemplateNode} node
   * @param {BoundaryProps} props
   * @param {((anchor: Node) => void)} children
   */
  constructor(t, n, i) {
    C(this, F);
    /** @type {Boundary | null} */
    M(this, "parent");
    C(this, $e, !1);
    /** @type {TemplateNode} */
    C(this, le);
    /** @type {TemplateNode | null} */
    C(this, Dt, y ? x : null);
    /** @type {BoundaryProps} */
    C(this, Ce);
    /** @type {((anchor: Node) => void)} */
    C(this, st);
    /** @type {Effect} */
    C(this, qe);
    /** @type {Effect | null} */
    C(this, he, null);
    /** @type {Effect | null} */
    C(this, te, null);
    /** @type {Effect | null} */
    C(this, Ae, null);
    /** @type {DocumentFragment | null} */
    C(this, Ue, null);
    C(this, at, 0);
    C(this, We, 0);
    C(this, lt, !1);
    /**
     * A source containing the number of pending async deriveds/expressions.
     * Only created if `$effect.pending()` is used inside the boundary,
     * otherwise updating the source results in needless `Batch.ensure()`
     * calls followed by no-op flushes
     * @type {Source<number> | null}
     */
    C(this, Xe, null);
    C(this, ln, () => {
      u(this, Xe) && nn(u(this, Xe), u(this, at));
    });
    C(this, on, Ui(() => (m(this, Xe, dt(u(this, at))), () => {
      m(this, Xe, null);
    })));
    m(this, le, t), m(this, Ce, n), m(this, st, i), this.parent = /** @type {Effect} */
    k.b, m(this, $e, !!u(this, Ce).pending), m(this, qe, pn(() => {
      if (k.b = this, y) {
        const r = u(this, Dt);
        qt(), /** @type {Comment} */
        r.nodeType === Nt && /** @type {Comment} */
        r.data === fn ? j(this, F, Sr).call(this) : j(this, F, Tr).call(this);
      } else {
        try {
          m(this, he, pe(() => i(u(this, le))));
        } catch (r) {
          this.error(r);
        }
        u(this, We) > 0 ? j(this, F, Xt).call(this) : m(this, $e, !1);
      }
    }, Wi)), y && m(this, le, x);
  }
  /**
   * Returns `true` if the effect exists inside a boundary whose pending snippet is shown
   * @returns {boolean}
   */
  is_pending() {
    return u(this, $e) || !!this.parent && this.parent.is_pending();
  }
  has_pending_snippet() {
    return !!u(this, Ce).pending;
  }
  /**
   * Update the source that powers `$effect.pending()` inside this boundary,
   * and controls when the current `pending` snippet (if any) is removed.
   * Do not call from inside the class
   * @param {1 | -1} d
   */
  update_pending_count(t) {
    j(this, F, Sn).call(this, t), m(this, at, u(this, at) + t), En.add(u(this, ln));
  }
  get_effect_pending() {
    return u(this, on).call(this), _(
      /** @type {Source<number>} */
      u(this, Xe)
    );
  }
  /** @param {unknown} error */
  error(t) {
    var n = u(this, Ce).onerror;
    let i = u(this, Ce).failed;
    if (u(this, lt) || !n && !i)
      throw t;
    u(this, he) && (G(u(this, he)), m(this, he, null)), u(this, te) && (G(u(this, te)), m(this, te, null)), u(this, Ae) && (G(u(this, Ae)), m(this, Ae, null)), y && (P(
      /** @type {TemplateNode} */
      u(this, Dt)
    ), Li(), P(tn()));
    var r = !1, s = !1;
    const a = () => {
      if (r) {
        Di();
        return;
      }
      r = !0, s && zi(), Le.ensure(), m(this, at, 0), u(this, Ae) !== null && yt(u(this, Ae), () => {
        m(this, Ae, null);
      }), m(this, $e, this.has_pending_snippet()), m(this, he, j(this, F, Wt).call(this, () => (m(this, lt, !1), pe(() => u(this, st).call(this, u(this, le)))))), u(this, We) > 0 ? j(this, F, Xt).call(this) : m(this, $e, !1);
    };
    var l = E;
    try {
      V(null), s = !0, n == null || n(t, a), s = !1;
    } catch (o) {
      Ot(o, u(this, qe) && u(this, qe).parent);
    } finally {
      V(l);
    }
    i && dn(() => {
      m(this, Ae, j(this, F, Wt).call(this, () => {
        m(this, lt, !0);
        try {
          return pe(() => {
            i(
              u(this, le),
              () => t,
              () => a
            );
          });
        } catch (o) {
          return Ot(
            o,
            /** @type {Effect} */
            u(this, qe).parent
          ), null;
        } finally {
          m(this, lt, !1);
        }
      }));
    });
  }
}
$e = new WeakMap(), le = new WeakMap(), Dt = new WeakMap(), Ce = new WeakMap(), st = new WeakMap(), qe = new WeakMap(), he = new WeakMap(), te = new WeakMap(), Ae = new WeakMap(), Ue = new WeakMap(), at = new WeakMap(), We = new WeakMap(), lt = new WeakMap(), Xe = new WeakMap(), ln = new WeakMap(), on = new WeakMap(), F = new WeakSet(), Tr = function() {
  try {
    m(this, he, pe(() => u(this, st).call(this, u(this, le))));
  } catch (t) {
    this.error(t);
  }
  m(this, $e, !1);
}, Sr = function() {
  const t = u(this, Ce).pending;
  t && (m(this, te, pe(() => t(u(this, le)))), Le.enqueue(() => {
    m(this, he, j(this, F, Wt).call(this, () => (Le.ensure(), pe(() => u(this, st).call(this, u(this, le)))))), u(this, We) > 0 ? j(this, F, Xt).call(this) : (yt(
      /** @type {Effect} */
      u(this, te),
      () => {
        m(this, te, null);
      }
    ), m(this, $e, !1));
  }));
}, /**
 * @param {() => Effect | null} fn
 */
Wt = function(t) {
  var n = k, i = E, r = ue;
  ge(u(this, qe)), V(u(this, qe)), At(u(this, qe).ctx);
  try {
    return t();
  } catch (s) {
    return yr(s), null;
  } finally {
    ge(n), V(i), At(r);
  }
}, Xt = function() {
  const t = (
    /** @type {(anchor: Node) => void} */
    u(this, Ce).pending
  );
  u(this, he) !== null && (m(this, Ue, document.createDocumentFragment()), Ur(u(this, he), u(this, Ue))), u(this, te) === null && m(this, te, pe(() => t(u(this, le))));
}, /**
 * Updates the pending count associated with the currently visible pending snippet,
 * if any, such that we can replace the snippet with content once work is done
 * @param {1 | -1} d
 */
Sn = function(t) {
  var n;
  if (!this.has_pending_snippet()) {
    this.parent && j(n = this.parent, F, Sn).call(n, t);
    return;
  }
  m(this, We, u(this, We) + t), u(this, We) === 0 && (m(this, $e, !1), u(this, te) && yt(u(this, te), () => {
    m(this, te, null);
  }), u(this, Ue) && (u(this, le).before(u(this, Ue)), m(this, Ue, null)));
};
function Gi(e, t, n) {
  const i = vn;
  if (t.length === 0) {
    n(e.map(i));
    return;
  }
  var r = R, s = (
    /** @type {Effect} */
    k
  ), a = Ji(), l = y;
  Promise.all(t.map((o) => /* @__PURE__ */ Zi(o))).then((o) => {
    a();
    try {
      n([...e.map(i), ...o]);
    } catch (f) {
      (s.f & De) === 0 && Ot(f, s);
    }
    l && K(!1), r == null || r.deactivate(), Cn();
  }).catch((o) => {
    Ot(o, s);
  });
}
function Ji() {
  var e = k, t = E, n = ue, i = R, r = y;
  if (r)
    var s = x;
  return function() {
    ge(e), V(t), At(n), i == null || i.activate(), r && (K(!0), P(s));
  };
}
function Cn() {
  ge(null), V(null), At(null);
}
// @__NO_SIDE_EFFECTS__
function vn(e) {
  var t = H | ne, n = E !== null && (E.f & H) !== 0 ? (
    /** @type {Derived} */
    E
  ) : null;
  return k === null || n !== null && (n.f & _e) !== 0 ? t |= _e : k.f |= vt, {
    ctx: ue,
    deps: null,
    effects: null,
    equals: _r,
    f: t,
    fn: e,
    reactions: null,
    rv: 0,
    v: (
      /** @type {V} */
      Y
    ),
    wv: 0,
    parent: n ?? k,
    ac: null
  };
}
// @__NO_SIDE_EFFECTS__
function Zi(e, t) {
  let n = (
    /** @type {Effect | null} */
    k
  );
  n === null && qi();
  var i = (
    /** @type {Boundary} */
    n.b
  ), r = (
    /** @type {Promise<V>} */
    /** @type {unknown} */
    void 0
  ), s = dt(
    /** @type {V} */
    Y
  ), a = !E, l = /* @__PURE__ */ new Map();
  return ls(() => {
    var d;
    var o = vr();
    r = o.promise;
    try {
      Promise.resolve(e()).then(o.resolve, o.reject).then(() => {
        f === R && f.committed && f.deactivate(), Cn();
      });
    } catch (h) {
      o.reject(h), Cn();
    }
    var f = (
      /** @type {Batch} */
      R
    );
    if (a) {
      var c = !i.is_pending();
      i.update_pending_count(1), f.increment(c), (d = l.get(f)) == null || d.reject(mt), l.delete(f), l.set(f, o);
    }
    const v = (h, p = void 0) => {
      if (f.activate(), p)
        p !== mt && (s.f |= ot, nn(s, p));
      else {
        (s.f & ot) !== 0 && (s.f ^= ot), nn(s, h);
        for (const [w, b] of l) {
          if (l.delete(w), w === f) break;
          b.reject(mt);
        }
      }
      a && (i.update_pending_count(-1), f.decrement(c));
    };
    o.promise.then(v, (h) => v(null, h || "unknown"));
  }), zr(() => {
    for (const o of l.values())
      o.reject(mt);
  }), new Promise((o) => {
    function f(c) {
      function v() {
        c === r ? o(s) : f(r);
      }
      c.then(v, v);
    }
    f(r);
  });
}
// @__NO_SIDE_EFFECTS__
function Vt(e) {
  const t = /* @__PURE__ */ vn(e);
  return Wr(t), t;
}
// @__NO_SIDE_EFFECTS__
function Qi(e) {
  const t = /* @__PURE__ */ vn(e);
  return t.equals = gr, t;
}
function Cr(e) {
  var t = e.effects;
  if (t !== null) {
    e.effects = null;
    for (var n = 0; n < t.length; n += 1)
      G(
        /** @type {Effect} */
        t[n]
      );
  }
}
function es(e) {
  for (var t = e.parent; t !== null; ) {
    if ((t.f & H) === 0)
      return (
        /** @type {Effect} */
        t
      );
    t = t.parent;
  }
  return null;
}
function Un(e) {
  var t, n = k;
  ge(es(e));
  try {
    e.f &= ~en, Cr(e), t = Jr(e);
  } finally {
    ge(n);
  }
  return t;
}
function qr(e) {
  var t = Un(e);
  if (e.equals(t) || (e.v = t, e.wv = Kr()), !pt)
    if (D !== null)
      D.set(e, e.v);
    else {
      var n = (Ke || (e.f & _e) !== 0) && e.deps !== null ? Qe : X;
      Z(e, n);
    }
}
const Ge = /* @__PURE__ */ new Map();
function dt(e, t) {
  var n = {
    f: 0,
    // TODO ideally we could skip this altogether, but it causes type errors
    v: e,
    reactions: null,
    equals: _r,
    rv: 0,
    wv: 0
  };
  return n;
}
// @__NO_SIDE_EFFECTS__
function U(e, t) {
  const n = dt(e);
  return Wr(n), n;
}
// @__NO_SIDE_EFFECTS__
function Ar(e, t = !1, n = !0) {
  const i = dt(e);
  return t || (i.equals = gr), i;
}
function A(e, t, n = !1) {
  E !== null && // since we are untracking the function inside `$inspect.with` we need to add this check
  // to ensure we error if state is set inside an inspect effect
  (!xe || (E.f & tr) !== 0) && mr() && (E.f & (H | ht | Bn | tr)) !== 0 && !(J != null && J.includes(e)) && Pi();
  let i = n ? Rt(t) : t;
  return nn(e, i);
}
function nn(e, t) {
  if (!e.equals(t)) {
    var n = e.v;
    pt ? Ge.set(e, t) : Ge.set(e, n), e.v = t;
    var i = Le.ensure();
    i.capture(e, n), (e.f & H) !== 0 && ((e.f & ne) !== 0 && Un(
      /** @type {Derived} */
      e
    ), Z(e, (e.f & _e) === 0 ? X : Qe)), e.wv = Kr(), Or(e, ne), k !== null && (k.f & X) !== 0 && (k.f & (Fe | Ze)) === 0 && (ce === null ? us([e]) : ce.push(e));
  }
  return t;
}
function It(e) {
  A(e, e.v + 1);
}
function Or(e, t) {
  var n = e.reactions;
  if (n !== null)
    for (var i = n.length, r = 0; r < i; r++) {
      var s = n[r], a = s.f, l = (a & ne) === 0;
      l && Z(s, t), (a & H) !== 0 ? (a & en) === 0 && (s.f |= en, Or(
        /** @type {Derived} */
        s,
        Qe
      )) : l && ((a & ht) !== 0 && ye !== null && ye.add(
        /** @type {Effect} */
        s
      ), ct(
        /** @type {Effect} */
        s
      ));
    }
}
function Rt(e) {
  if (typeof e != "object" || e === null || Ut in e)
    return e;
  const t = hr(e);
  if (t !== yi && t !== bi)
    return e;
  var n = /* @__PURE__ */ new Map(), i = Pn(e), r = /* @__PURE__ */ U(0), s = ft, a = (l) => {
    if (ft === s)
      return l();
    var o = E, f = ft;
    V(null), ar(s);
    var c = l();
    return V(o), ar(f), c;
  };
  return i && n.set("length", /* @__PURE__ */ U(
    /** @type {any[]} */
    e.length
  )), new Proxy(
    /** @type {any} */
    e,
    {
      defineProperty(l, o, f) {
        (!("value" in f) || f.configurable === !1 || f.enumerable === !1 || f.writable === !1) && Mi();
        var c = n.get(o);
        return c === void 0 ? c = a(() => {
          var v = /* @__PURE__ */ U(f.value);
          return n.set(o, v), v;
        }) : A(c, f.value, !0), !0;
      },
      deleteProperty(l, o) {
        var f = n.get(o);
        if (f === void 0) {
          if (o in l) {
            const c = a(() => /* @__PURE__ */ U(Y));
            n.set(o, c), It(r);
          }
        } else
          A(f, Y), It(r);
        return !0;
      },
      get(l, o, f) {
        var h;
        if (o === Ut)
          return e;
        var c = n.get(o), v = o in l;
        if (c === void 0 && (!v || (h = wt(l, o)) != null && h.writable) && (c = a(() => {
          var p = Rt(v ? l[o] : Y), w = /* @__PURE__ */ U(p);
          return w;
        }), n.set(o, c)), c !== void 0) {
          var d = _(c);
          return d === Y ? void 0 : d;
        }
        return Reflect.get(l, o, f);
      },
      getOwnPropertyDescriptor(l, o) {
        var f = Reflect.getOwnPropertyDescriptor(l, o);
        if (f && "value" in f) {
          var c = n.get(o);
          c && (f.value = _(c));
        } else if (f === void 0) {
          var v = n.get(o), d = v == null ? void 0 : v.v;
          if (v !== void 0 && d !== Y)
            return {
              enumerable: !0,
              configurable: !0,
              value: d,
              writable: !0
            };
        }
        return f;
      },
      has(l, o) {
        var d;
        if (o === Ut)
          return !0;
        var f = n.get(o), c = f !== void 0 && f.v !== Y || Reflect.has(l, o);
        if (f !== void 0 || k !== null && (!c || (d = wt(l, o)) != null && d.writable)) {
          f === void 0 && (f = a(() => {
            var h = c ? Rt(l[o]) : Y, p = /* @__PURE__ */ U(h);
            return p;
          }), n.set(o, f));
          var v = _(f);
          if (v === Y)
            return !1;
        }
        return c;
      },
      set(l, o, f, c) {
        var S;
        var v = n.get(o), d = o in l;
        if (i && o === "length")
          for (var h = f; h < /** @type {Source<number>} */
          v.v; h += 1) {
            var p = n.get(h + "");
            p !== void 0 ? A(p, Y) : h in l && (p = a(() => /* @__PURE__ */ U(Y)), n.set(h + "", p));
          }
        if (v === void 0)
          (!d || (S = wt(l, o)) != null && S.writable) && (v = a(() => /* @__PURE__ */ U(void 0)), A(v, Rt(f)), n.set(o, v));
        else {
          d = v.v !== Y;
          var w = a(() => Rt(f));
          A(v, w);
        }
        var b = Reflect.getOwnPropertyDescriptor(l, o);
        if (b != null && b.set && b.set.call(c, f), !d) {
          if (i && typeof o == "string") {
            var z = (
              /** @type {Source<number>} */
              n.get("length")
            ), N = Number(o);
            Number.isInteger(N) && N >= z.v && A(z, N + 1);
          }
          It(r);
        }
        return !0;
      },
      ownKeys(l) {
        _(r);
        var o = Reflect.ownKeys(l).filter((v) => {
          var d = n.get(v);
          return d === void 0 || d.v !== Y;
        });
        for (var [f, c] of n)
          c.v !== Y && !(f in l) && o.push(f);
        return o;
      },
      setPrototypeOf() {
        Ii();
      }
    }
  );
}
var rr, Nr, Rr, jr;
function qn() {
  if (rr === void 0) {
    rr = window, Nr = /Firefox/.test(navigator.userAgent);
    var e = Element.prototype, t = Node.prototype, n = Text.prototype;
    Rr = wt(t, "firstChild").get, jr = wt(t, "nextSibling").get, er(e) && (e.__click = void 0, e.__className = void 0, e.__attributes = null, e.__style = void 0, e.__e = void 0), er(n) && (n.__t = void 0);
  }
}
function ke(e = "") {
  return document.createTextNode(e);
}
// @__NO_SIDE_EFFECTS__
function Je(e) {
  return Rr.call(e);
}
// @__NO_SIDE_EFFECTS__
function Re(e) {
  return jr.call(e);
}
function Ye(e, t) {
  if (!y)
    return /* @__PURE__ */ Je(e);
  var n = (
    /** @type {TemplateNode} */
    /* @__PURE__ */ Je(x)
  );
  if (n === null)
    n = x.appendChild(ke());
  else if (t && n.nodeType !== Yn) {
    var i = ke();
    return n == null || n.before(i), P(i), i;
  }
  return P(n), n;
}
function ts(e, t = !1) {
  if (!y) {
    var n = (
      /** @type {DocumentFragment} */
      /* @__PURE__ */ Je(
        /** @type {Node} */
        e
      )
    );
    return n instanceof Comment && n.data === "" ? /* @__PURE__ */ Re(n) : n;
  }
  if (t && (x == null ? void 0 : x.nodeType) !== Yn) {
    var i = ke();
    return x == null || x.before(i), P(i), i;
  }
  return x;
}
function Kt(e, t = 1, n = !1) {
  let i = y ? x : e;
  for (var r; t--; )
    r = i, i = /** @type {TemplateNode} */
    /* @__PURE__ */ Re(i);
  if (!y)
    return i;
  if (n && (i == null ? void 0 : i.nodeType) !== Yn) {
    var s = ke();
    return i === null ? r == null || r.after(s) : i.before(s), P(s), s;
  }
  return P(i), /** @type {TemplateNode} */
  i;
}
function Mr(e) {
  e.textContent = "";
}
function Ir() {
  return !1;
}
function Pr(e) {
  var t = E, n = k;
  V(null), ge(null);
  try {
    return e();
  } finally {
    V(t), ge(n);
  }
}
function ns(e) {
  k === null && E === null && Ni(), E !== null && (E.f & _e) !== 0 && k === null && Oi(), pt && Ai();
}
function rs(e, t) {
  var n = t.last;
  n === null ? t.last = t.first = e : (n.next = e, e.prev = n, t.last = e);
}
function je(e, t, n, i = !0) {
  var r = k;
  r !== null && (r.f & fe) !== 0 && (e |= fe);
  var s = {
    ctx: ue,
    deps: null,
    nodes_start: null,
    nodes_end: null,
    f: e | ne,
    first: null,
    fn: t,
    last: null,
    next: null,
    parent: r,
    b: r && r.b,
    prev: null,
    teardown: null,
    transitions: null,
    wv: 0,
    ac: null
  };
  if (n)
    try {
      sn(s), s.f |= Fn;
    } catch (o) {
      throw G(s), o;
    }
  else t !== null && ct(s);
  if (i) {
    var a = s;
    if (n && a.deps === null && a.teardown === null && a.nodes_start === null && a.first === a.last && // either `null`, or a singular child
    (a.f & vt) === 0 && (a = a.first), a !== null && (a.parent = r, r !== null && rs(a, r), E !== null && (E.f & H) !== 0 && (e & Ze) === 0)) {
      var l = (
        /** @type {Derived} */
        E
      );
      (l.effects ?? (l.effects = [])).push(a);
    }
  }
  return s;
}
function is() {
  return E !== null && !xe;
}
function zr(e) {
  const t = je(Ln, null, !1);
  return Z(t, X), t.teardown = e, t;
}
function Gt(e) {
  ns();
  var t = (
    /** @type {Effect} */
    k.f
  ), n = !E && (t & Fe) !== 0 && (t & Fn) === 0;
  if (n) {
    var i = (
      /** @type {ComponentContext} */
      ue
    );
    (i.e ?? (i.e = [])).push(e);
  } else
    return Dr(e);
}
function Dr(e) {
  return je(Dn | xi, e, !1);
}
function ss(e) {
  Le.ensure();
  const t = je(Ze | vt, e, !0);
  return () => {
    G(t);
  };
}
function as(e) {
  Le.ensure();
  const t = je(Ze | vt, e, !0);
  return (n = {}) => new Promise((i) => {
    n.outro ? yt(t, () => {
      G(t), i(void 0);
    }) : (G(t), i(void 0));
  });
}
function Lr(e) {
  return je(Dn, e, !1);
}
function ls(e) {
  return je(Bn | vt, e, !0);
}
function Wn(e, t = 0) {
  return je(Ln | t, e, !0);
}
function Ve(e, t = [], n = []) {
  Gi(t, n, (i) => {
    je(Ln, () => e(...i.map(_)), !0);
  });
}
function pn(e, t = 0) {
  var n = je(ht | t, e, !0);
  return n;
}
function pe(e, t = !0) {
  return je(Fe | vt, e, !0, t);
}
function Fr(e) {
  var t = e.teardown;
  if (t !== null) {
    const n = pt, i = E;
    sr(!0), V(null);
    try {
      t.call(null);
    } finally {
      sr(n), V(i);
    }
  }
}
function Br(e, t = !1) {
  var n = e.first;
  for (e.first = e.last = null; n !== null; ) {
    const r = n.ac;
    r !== null && Pr(() => {
      r.abort(mt);
    });
    var i = n.next;
    (n.f & Ze) !== 0 ? n.parent = null : G(n, t), n = i;
  }
}
function os(e) {
  for (var t = e.first; t !== null; ) {
    var n = t.next;
    (t.f & Fe) === 0 && G(t), t = n;
  }
}
function G(e, t = !0) {
  var n = !1;
  (t || (e.f & Ei) !== 0) && e.nodes_start !== null && e.nodes_end !== null && (fs(
    e.nodes_start,
    /** @type {TemplateNode} */
    e.nodes_end
  ), n = !0), Br(e, t && !n), rn(e, 0), Z(e, De);
  var i = e.transitions;
  if (i !== null)
    for (const s of i)
      s.stop();
  Fr(e);
  var r = e.parent;
  r !== null && r.first !== null && Yr(e), e.next = e.prev = e.teardown = e.ctx = e.deps = e.fn = e.nodes_start = e.nodes_end = e.ac = null;
}
function fs(e, t) {
  for (; e !== null; ) {
    var n = e === t ? null : (
      /** @type {TemplateNode} */
      /* @__PURE__ */ Re(e)
    );
    e.remove(), e = n;
  }
}
function Yr(e) {
  var t = e.parent, n = e.prev, i = e.next;
  n !== null && (n.next = i), i !== null && (i.prev = n), t !== null && (t.first === e && (t.first = i), t.last === e && (t.last = n));
}
function yt(e, t, n = !0) {
  var i = [];
  Xn(e, i, !0), Vr(i, () => {
    n && G(e), t && t();
  });
}
function Vr(e, t) {
  var n = e.length;
  if (n > 0) {
    var i = () => --n || t();
    for (var r of e)
      r.out(i);
  } else
    t();
}
function Xn(e, t, n) {
  if ((e.f & fe) === 0) {
    if (e.f ^= fe, e.transitions !== null)
      for (const a of e.transitions)
        (a.is_global || n) && t.push(a);
    for (var i = e.first; i !== null; ) {
      var r = i.next, s = (i.f & Bt) !== 0 || (i.f & Fe) !== 0;
      Xn(i, t, s ? n : !1), i = r;
    }
  }
}
function Kn(e) {
  Hr(e, !0);
}
function Hr(e, t) {
  if ((e.f & fe) !== 0) {
    e.f ^= fe, (e.f & X) === 0 && (Z(e, ne), ct(e));
    for (var n = e.first; n !== null; ) {
      var i = n.next, r = (n.f & Bt) !== 0 || (n.f & Fe) !== 0;
      Hr(n, r ? t : !1), n = i;
    }
    if (e.transitions !== null)
      for (const s of e.transitions)
        (s.is_global || t) && s.in();
  }
}
function Ur(e, t) {
  for (var n = e.nodes_start, i = e.nodes_end; n !== null; ) {
    var r = n === i ? null : (
      /** @type {TemplateNode} */
      /* @__PURE__ */ Re(n)
    );
    t.append(n), n = r;
  }
}
let bt = !1;
function ir(e) {
  bt = e;
}
let pt = !1;
function sr(e) {
  pt = e;
}
let E = null, xe = !1;
function V(e) {
  E = e;
}
let k = null;
function ge(e) {
  k = e;
}
let J = null;
function Wr(e) {
  E !== null && (J === null ? J = [e] : J.push(e));
}
let W = null, ae = 0, ce = null;
function us(e) {
  ce = e;
}
let Xr = 1, Pt = 0, ft = Pt;
function ar(e) {
  ft = e;
}
let Ke = !1;
function Kr() {
  return ++Xr;
}
function _n(e) {
  var v;
  var t = e.f;
  if ((t & ne) !== 0)
    return !0;
  if ((t & Qe) !== 0) {
    var n = e.deps, i = (t & _e) !== 0;
    if (t & H && (e.f &= ~en), n !== null) {
      var r, s, a = (t & Qt) !== 0, l = i && k !== null && !Ke, o = n.length;
      if ((a || l) && (k === null || (k.f & De) === 0)) {
        var f = (
          /** @type {Derived} */
          e
        ), c = f.parent;
        for (r = 0; r < o; r++)
          s = n[r], (a || !((v = s == null ? void 0 : s.reactions) != null && v.includes(f))) && (s.reactions ?? (s.reactions = [])).push(f);
        a && (f.f ^= Qt), l && c !== null && (c.f & _e) === 0 && (f.f ^= _e);
      }
      for (r = 0; r < o; r++)
        if (s = n[r], _n(
          /** @type {Derived} */
          s
        ) && qr(
          /** @type {Derived} */
          s
        ), s.wv > e.wv)
          return !0;
    }
    (!i || k !== null && !Ke) && Z(e, X);
  }
  return !1;
}
function Gr(e, t, n = !0) {
  var i = e.reactions;
  if (i !== null && !(J != null && J.includes(e)))
    for (var r = 0; r < i.length; r++) {
      var s = i[r];
      (s.f & H) !== 0 ? Gr(
        /** @type {Derived} */
        s,
        t,
        !1
      ) : t === s && (n ? Z(s, ne) : (s.f & X) !== 0 && Z(s, Qe), ct(
        /** @type {Effect} */
        s
      ));
    }
}
function Jr(e) {
  var w;
  var t = W, n = ae, i = ce, r = E, s = Ke, a = J, l = ue, o = xe, f = ft, c = e.f;
  W = /** @type {null | Value[]} */
  null, ae = 0, ce = null, Ke = (c & _e) !== 0 && (xe || !bt || E === null), E = (c & (Fe | Ze)) === 0 ? e : null, J = null, At(e.ctx), xe = !1, ft = ++Pt, e.ac !== null && (Pr(() => {
    e.ac.abort(mt);
  }), e.ac = null);
  try {
    e.f |= $n;
    var v = (
      /** @type {Function} */
      e.fn
    ), d = v(), h = e.deps;
    if (W !== null) {
      var p;
      if (rn(e, ae), h !== null && ae > 0)
        for (h.length = ae + W.length, p = 0; p < W.length; p++)
          h[ae + p] = W[p];
      else
        e.deps = h = W;
      if (!Ke || // Deriveds that already have reactions can cleanup, so we still add them as reactions
      (c & H) !== 0 && /** @type {import('#client').Derived} */
      e.reactions !== null)
        for (p = ae; p < h.length; p++)
          ((w = h[p]).reactions ?? (w.reactions = [])).push(e);
    } else h !== null && ae < h.length && (rn(e, ae), h.length = ae);
    if (mr() && ce !== null && !xe && h !== null && (e.f & (H | Qe | ne)) === 0)
      for (p = 0; p < /** @type {Source[]} */
      ce.length; p++)
        Gr(
          ce[p],
          /** @type {Effect} */
          e
        );
    return r !== null && r !== e && (Pt++, ce !== null && (i === null ? i = ce : i.push(.../** @type {Source[]} */
    ce))), (e.f & ot) !== 0 && (e.f ^= ot), d;
  } catch (b) {
    return yr(b);
  } finally {
    e.f ^= $n, W = t, ae = n, ce = i, E = r, Ke = s, J = a, At(l), xe = o, ft = f;
  }
}
function cs(e, t) {
  let n = t.reactions;
  if (n !== null) {
    var i = mi.call(n, e);
    if (i !== -1) {
      var r = n.length - 1;
      r === 0 ? n = t.reactions = null : (n[i] = n[r], n.pop());
    }
  }
  n === null && (t.f & H) !== 0 && // Destroying a child effect while updating a parent effect can cause a dependency to appear
  // to be unused, when in fact it is used by the currently-updating parent. Checking `new_deps`
  // allows us to skip the expensive work of disconnecting and immediately reconnecting it
  (W === null || !W.includes(t)) && (Z(t, Qe), (t.f & (_e | Qt)) === 0 && (t.f ^= Qt), Cr(
    /** @type {Derived} **/
    t
  ), rn(
    /** @type {Derived} **/
    t,
    0
  ));
}
function rn(e, t) {
  var n = e.deps;
  if (n !== null)
    for (var i = t; i < n.length; i++)
      cs(e, n[i]);
}
function sn(e) {
  var t = e.f;
  if ((t & De) === 0) {
    Z(e, X);
    var n = k, i = bt;
    k = e, bt = !0;
    try {
      (t & ht) !== 0 ? os(e) : Br(e), Fr(e);
      var r = Jr(e);
      e.teardown = typeof r == "function" ? r : null, e.wv = Xr;
      var s;
      dr && Bi && (e.f & ne) !== 0 && e.deps;
    } finally {
      bt = i, k = n;
    }
  }
}
function _(e) {
  var t = e.f, n = (t & H) !== 0;
  if (E !== null && !xe) {
    var i = k !== null && (k.f & De) !== 0;
    if (!i && !(J != null && J.includes(e))) {
      var r = E.deps;
      if ((E.f & $n) !== 0)
        e.rv < Pt && (e.rv = Pt, W === null && r !== null && r[ae] === e ? ae++ : W === null ? W = [e] : (!Ke || !W.includes(e)) && W.push(e));
      else {
        (E.deps ?? (E.deps = [])).push(e);
        var s = e.reactions;
        s === null ? e.reactions = [E] : s.includes(E) || s.push(E);
      }
    }
  } else if (n && /** @type {Derived} */
  e.deps === null && /** @type {Derived} */
  e.effects === null) {
    var a = (
      /** @type {Derived} */
      e
    ), l = a.parent;
    l !== null && (l.f & _e) === 0 && (a.f ^= _e);
  }
  if (pt) {
    if (Ge.has(e))
      return Ge.get(e);
    if (n) {
      a = /** @type {Derived} */
      e;
      var o = a.v;
      return ((a.f & X) === 0 && a.reactions !== null || Zr(a)) && (o = Un(a)), Ge.set(a, o), o;
    }
  } else if (n) {
    if (a = /** @type {Derived} */
    e, D != null && D.has(a))
      return D.get(a);
    _n(a) && qr(a);
  }
  if (D != null && D.has(e))
    return D.get(e);
  if ((e.f & ot) !== 0)
    throw e.v;
  return e.v;
}
function Zr(e) {
  if (e.v === Y) return !0;
  if (e.deps === null) return !1;
  for (const t of e.deps)
    if (Ge.has(t) || (t.f & H) !== 0 && Zr(
      /** @type {Derived} */
      t
    ))
      return !0;
  return !1;
}
function Gn(e) {
  var t = xe;
  try {
    return xe = !0, e();
  } finally {
    xe = t;
  }
}
const ds = -7169;
function Z(e, t) {
  e.f = e.f & ds | t;
}
const Qr = /* @__PURE__ */ new Set(), An = /* @__PURE__ */ new Set();
function hs(e) {
  for (var t = 0; t < e.length; t++)
    Qr.add(e[t]);
  for (var n of An)
    n(e);
}
let lr = null;
function Ht(e) {
  var N;
  var t = this, n = (
    /** @type {Node} */
    t.ownerDocument
  ), i = e.type, r = ((N = e.composedPath) == null ? void 0 : N.call(e)) || [], s = (
    /** @type {null | Element} */
    r[0] || e.target
  );
  lr = e;
  var a = 0, l = lr === e && e.__root;
  if (l) {
    var o = r.indexOf(l);
    if (o !== -1 && (t === document || t === /** @type {any} */
    window)) {
      e.__root = t;
      return;
    }
    var f = r.indexOf(t);
    if (f === -1)
      return;
    o <= f && (a = o);
  }
  if (s = /** @type {Element} */
  r[a] || e.target, s !== t) {
    Ct(e, "currentTarget", {
      configurable: !0,
      get() {
        return s || n;
      }
    });
    var c = E, v = k;
    V(null), ge(null);
    try {
      for (var d, h = []; s !== null; ) {
        var p = s.assignedSlot || s.parentNode || /** @type {any} */
        s.host || null;
        try {
          var w = s["__" + i];
          if (w != null && (!/** @type {any} */
          s.disabled || // DOM could've been updated already by the time this is reached, so we check this as well
          // -> the target could not have been disabled because it emits the event in the first place
          e.target === s))
            if (Pn(w)) {
              var [b, ...z] = w;
              b.apply(s, [e, ...z]);
            } else
              w.call(s, e);
        } catch (S) {
          d ? h.push(S) : d = S;
        }
        if (e.cancelBubble || p === t || p === null)
          break;
        s = p;
      }
      if (d) {
        for (let S of h)
          queueMicrotask(() => {
            throw S;
          });
        throw d;
      }
    } finally {
      e.__root = t, delete e.currentTarget, V(c), ge(v);
    }
  }
}
function vs(e) {
  var t = document.createElement("template");
  return t.innerHTML = e.replaceAll("<!>", "<!---->"), t.content;
}
function ut(e, t) {
  var n = (
    /** @type {Effect} */
    k
  );
  n.nodes_start === null && (n.nodes_start = e, n.nodes_end = t);
}
// @__NO_SIDE_EFFECTS__
function _t(e, t) {
  var n = (t & vi) !== 0, i = (t & pi) !== 0, r, s = !e.startsWith("<!>");
  return () => {
    if (y)
      return ut(x, null), x;
    r === void 0 && (r = vs(s ? e : "<!>" + e), n || (r = /** @type {Node} */
    /* @__PURE__ */ Je(r)));
    var a = (
      /** @type {TemplateNode} */
      i || Nr ? document.importNode(r, !0) : r.cloneNode(!0)
    );
    if (n) {
      var l = (
        /** @type {TemplateNode} */
        /* @__PURE__ */ Je(a)
      ), o = (
        /** @type {TemplateNode} */
        a.lastChild
      );
      ut(l, o);
    } else
      ut(a, a);
    return a;
  };
}
function ps() {
  if (y)
    return ut(x, null), x;
  var e = document.createDocumentFragment(), t = document.createComment(""), n = ke();
  return e.append(t, n), ut(t, n), e;
}
function Ie(e, t) {
  if (y) {
    k.nodes_end = x, qt();
    return;
  }
  e !== null && e.before(
    /** @type {Node} */
    t
  );
}
const _s = ["touchstart", "touchmove"];
function gs(e) {
  return _s.includes(e);
}
const ms = (
  /** @type {const} */
  ["textarea", "script", "style", "title"]
);
function ws(e) {
  return ms.includes(
    /** @type {typeof RAW_TEXT_ELEMENTS[number]} */
    e
  );
}
function ys(e, t) {
  var n = t == null ? "" : typeof t == "object" ? t + "" : t;
  n !== (e.__t ?? (e.__t = e.nodeValue)) && (e.__t = n, e.nodeValue = n + "");
}
function ei(e, t) {
  return ti(e, t);
}
function bs(e, t) {
  qn(), t.intro = t.intro ?? !1;
  const n = t.target, i = y, r = x;
  try {
    for (var s = (
      /** @type {TemplateNode} */
      /* @__PURE__ */ Je(n)
    ); s && (s.nodeType !== Nt || /** @type {Comment} */
    s.data !== cr); )
      s = /** @type {TemplateNode} */
      /* @__PURE__ */ Re(s);
    if (!s)
      throw St;
    K(!0), P(
      /** @type {Comment} */
      s
    );
    const a = ti(e, { ...t, anchor: s });
    return K(!1), /**  @type {Exports} */
    a;
  } catch (a) {
    if (a instanceof Error && a.message.split(`
`).some((l) => l.startsWith("https://svelte.dev/e/")))
      throw a;
    return a !== St && console.warn("Failed to hydrate: ", a), t.recover === !1 && ji(), qn(), Mr(n), K(!1), ei(e, t);
  } finally {
    K(i), P(r);
  }
}
const gt = /* @__PURE__ */ new Map();
function ti(e, { target: t, anchor: n, props: i = {}, events: r, context: s, intro: a = !0 }) {
  qn();
  var l = /* @__PURE__ */ new Set(), o = (v) => {
    for (var d = 0; d < v.length; d++) {
      var h = v[d];
      if (!l.has(h)) {
        l.add(h);
        var p = gs(h);
        t.addEventListener(h, Ht, { passive: p });
        var w = gt.get(h);
        w === void 0 ? (document.addEventListener(h, Ht, { passive: p }), gt.set(h, 1)) : gt.set(h, w + 1);
      }
    }
  };
  o(zn(Qr)), An.add(o);
  var f = void 0, c = as(() => {
    var v = n ?? t.appendChild(ke());
    return Xi(
      /** @type {TemplateNode} */
      v,
      {
        pending: () => {
        }
      },
      (d) => {
        if (s) {
          Vn({});
          var h = (
            /** @type {ComponentContext} */
            ue
          );
          h.c = s;
        }
        if (r && (i.$$events = r), y && ut(
          /** @type {TemplateNode} */
          d,
          null
        ), f = e(d, i) || {}, y && (k.nodes_end = x, x === null || x.nodeType !== Nt || /** @type {Comment} */
        x.data !== In))
          throw cn(), St;
        s && Hn();
      }
    ), () => {
      var p;
      for (var d of l) {
        t.removeEventListener(d, Ht);
        var h = (
          /** @type {number} */
          gt.get(d)
        );
        --h === 0 ? (document.removeEventListener(d, Ht), gt.delete(d)) : gt.set(d, h);
      }
      An.delete(o), v !== n && ((p = v.parentNode) == null || p.removeChild(v));
    };
  });
  return On.set(f, c), f;
}
let On = /* @__PURE__ */ new WeakMap();
function $s(e, t) {
  const n = On.get(e);
  return n ? (On.delete(e), n(t)) : Promise.resolve();
}
var Pe, Oe, Ee, Lt, Ft;
class ni {
  /**
   * @param {TemplateNode} anchor
   * @param {boolean} transition
   */
  constructor(t, n = !0) {
    /** @type {TemplateNode} */
    M(this, "anchor");
    /** @type {Map<Batch, Key>} */
    C(this, Pe, /* @__PURE__ */ new Map());
    /** @type {Map<Key, Effect>} */
    C(this, Oe, /* @__PURE__ */ new Map());
    /** @type {Map<Key, Branch>} */
    C(this, Ee, /* @__PURE__ */ new Map());
    /**
     * Whether to pause (i.e. outro) on change, or destroy immediately.
     * This is necessary for `<svelte:element>`
     */
    C(this, Lt, !0);
    C(this, Ft, () => {
      var t = (
        /** @type {Batch} */
        R
      );
      if (u(this, Pe).has(t)) {
        var n = (
          /** @type {Key} */
          u(this, Pe).get(t)
        ), i = u(this, Oe).get(n);
        if (i)
          Kn(i);
        else {
          var r = u(this, Ee).get(n);
          r && (u(this, Oe).set(n, r.effect), u(this, Ee).delete(n), r.fragment.lastChild.remove(), this.anchor.before(r.fragment), i = r.effect);
        }
        for (const [s, a] of u(this, Pe)) {
          if (u(this, Pe).delete(s), s === t)
            break;
          const l = u(this, Ee).get(a);
          l && (G(l.effect), u(this, Ee).delete(a));
        }
        for (const [s, a] of u(this, Oe)) {
          if (s === n) continue;
          const l = () => {
            if (Array.from(u(this, Pe).values()).includes(s)) {
              var f = document.createDocumentFragment();
              Ur(a, f), f.append(ke()), u(this, Ee).set(s, { effect: a, fragment: f });
            } else
              G(a);
            u(this, Oe).delete(s);
          };
          u(this, Lt) || !i ? yt(a, l, !1) : l();
        }
      }
    });
    this.anchor = t, m(this, Lt, n);
  }
  /**
   *
   * @param {any} key
   * @param {null | ((target: TemplateNode) => void)} fn
   */
  ensure(t, n) {
    var i = (
      /** @type {Batch} */
      R
    ), r = Ir();
    if (n && !u(this, Oe).has(t) && !u(this, Ee).has(t))
      if (r) {
        var s = document.createDocumentFragment(), a = ke();
        s.append(a), u(this, Ee).set(t, {
          effect: pe(() => n(a)),
          fragment: s
        });
      } else
        u(this, Oe).set(
          t,
          pe(() => n(this.anchor))
        );
    if (u(this, Pe).set(i, t), r) {
      for (const [l, o] of u(this, Oe))
        l === t ? i.skipped_effects.delete(o) : i.skipped_effects.add(o);
      for (const [l, o] of u(this, Ee))
        l === t ? i.skipped_effects.delete(o.effect) : i.skipped_effects.add(o.effect);
      i.add_callback(u(this, Ft));
    } else
      y && (this.anchor = x), u(this, Ft).call(this);
  }
}
Pe = new WeakMap(), Oe = new WeakMap(), Ee = new WeakMap(), Lt = new WeakMap(), Ft = new WeakMap();
function ri(e) {
  ue === null && Ci(), Gt(() => {
    const t = Gn(e);
    if (typeof t == "function") return (
      /** @type {() => void} */
      t
    );
  });
}
function jt(e, t, n = !1) {
  y && qt();
  var i = new ni(e), r = n ? Bt : 0;
  function s(a, l) {
    if (y) {
      const f = pr(e) === fn;
      if (a === f) {
        var o = tn();
        P(o), i.anchor = o, K(!1), i.ensure(a, l), K(!0);
        return;
      }
    }
    i.ensure(a, l);
  }
  pn(() => {
    var a = !1;
    t((l, o = !0) => {
      a = !0, s(o, l);
    }), a || s(!1, null);
  }, r);
}
function Es(e, t, n) {
  for (var i = e.items, r = [], s = t.length, a = 0; a < s; a++)
    Xn(t[a].e, r, !0);
  var l = s > 0 && r.length === 0 && n !== null;
  if (l) {
    var o = (
      /** @type {Element} */
      /** @type {Element} */
      n.parentNode
    );
    Mr(o), o.append(
      /** @type {Element} */
      n
    ), i.clear(), Se(e, t[0].prev, t[s - 1].next);
  }
  Vr(r, () => {
    for (var f = 0; f < s; f++) {
      var c = t[f];
      l || (i.delete(c.k), Se(e, c.prev, c.next)), G(c.e, !l);
    }
  });
}
function xs(e, t, n, i, r, s = null) {
  var a = e, l = { flags: t, items: /* @__PURE__ */ new Map(), first: null };
  {
    var o = (
      /** @type {Element} */
      e
    );
    a = y ? P(
      /** @type {Comment | Text} */
      /* @__PURE__ */ Je(o)
    ) : o.appendChild(ke());
  }
  y && qt();
  var f = null, c = !1, v = /* @__PURE__ */ new Map(), d = /* @__PURE__ */ Qi(() => {
    var b = n();
    return Pn(b) ? b : b == null ? [] : zn(b);
  }), h, p;
  function w() {
    ks(
      p,
      h,
      l,
      v,
      a,
      r,
      t,
      i,
      n
    ), s !== null && (h.length === 0 ? f ? Kn(f) : f = pe(() => s(a)) : f !== null && yt(f, () => {
      f = null;
    }));
  }
  pn(() => {
    p ?? (p = /** @type {Effect} */
    k), h = /** @type {V[]} */
    _(d);
    var b = h.length;
    if (c && b === 0)
      return;
    c = b === 0;
    let z = !1;
    if (y) {
      var N = pr(a) === fn;
      N !== (b === 0) && (a = tn(), P(a), K(!1), z = !0);
    }
    if (y) {
      for (var S = null, g, O = 0; O < b; O++) {
        if (x.nodeType === Nt && /** @type {Comment} */
        x.data === In) {
          a = /** @type {Comment} */
          x, z = !0, K(!1);
          break;
        }
        var Q = h[O], I = i(Q, O);
        g = Nn(
          x,
          l,
          S,
          null,
          Q,
          I,
          O,
          r,
          t,
          n
        ), l.items.set(I, g), S = g;
      }
      b > 0 && P(tn());
    }
    if (y)
      b === 0 && s && (f = pe(() => s(a)));
    else if (Ir()) {
      var me = /* @__PURE__ */ new Set(), re = (
        /** @type {Batch} */
        R
      );
      for (O = 0; O < b; O += 1) {
        Q = h[O], I = i(Q, O);
        var Te = l.items.get(I) ?? v.get(I);
        Te || (g = Nn(
          null,
          l,
          null,
          null,
          Q,
          I,
          O,
          r,
          t,
          n,
          !0
        ), v.set(I, g)), me.add(I);
      }
      for (const [Be, et] of l.items)
        me.has(Be) || re.skipped_effects.add(et.e);
      re.add_callback(w);
    } else
      w();
    z && K(!0), _(d);
  }), y && (a = x);
}
function ks(e, t, n, i, r, s, a, l, o) {
  var f = t.length, c = n.items, v = n.first, d = v, h, p = null, w = [], b = [], z, N, S, g;
  for (g = 0; g < f; g += 1) {
    if (z = t[g], N = l(z, g), S = c.get(N), S === void 0) {
      var O = i.get(N);
      if (O !== void 0) {
        i.delete(N), c.set(N, O);
        var Q = p ? p.next : d;
        Se(n, p, O), Se(n, O, Q), bn(O, Q, r), p = O;
      } else {
        var I = d ? (
          /** @type {TemplateNode} */
          d.e.nodes_start
        ) : r;
        p = Nn(
          I,
          n,
          p,
          p === null ? n.first : p.next,
          z,
          N,
          g,
          s,
          a,
          o
        );
      }
      c.set(N, p), w = [], b = [], d = p.next;
      continue;
    }
    if ((S.e.f & fe) !== 0 && Kn(S.e), S !== d) {
      if (h !== void 0 && h.has(S)) {
        if (w.length < b.length) {
          var me = b[0], re;
          p = me.prev;
          var Te = w[0], Be = w[w.length - 1];
          for (re = 0; re < w.length; re += 1)
            bn(w[re], me, r);
          for (re = 0; re < b.length; re += 1)
            h.delete(b[re]);
          Se(n, Te.prev, Be.next), Se(n, p, Te), Se(n, Be, me), d = me, p = Be, g -= 1, w = [], b = [];
        } else
          h.delete(S), bn(S, d, r), Se(n, S.prev, S.next), Se(n, S, p === null ? n.first : p.next), Se(n, p, S), p = S;
        continue;
      }
      for (w = [], b = []; d !== null && d.k !== N; )
        (d.e.f & fe) === 0 && (h ?? (h = /* @__PURE__ */ new Set())).add(d), b.push(d), d = d.next;
      if (d === null)
        continue;
      S = d;
    }
    w.push(S), p = S, d = S.next;
  }
  if (d !== null || h !== void 0) {
    for (var et = h === void 0 ? [] : zn(h); d !== null; )
      (d.e.f & fe) === 0 && et.push(d), d = d.next;
    var gn = et.length;
    if (gn > 0) {
      var mn = f === 0 ? r : null;
      Es(n, et, mn);
    }
  }
  e.first = n.first && n.first.e, e.last = p && p.e;
  for (var wn of i.values())
    G(wn.e);
  i.clear();
}
function Nn(e, t, n, i, r, s, a, l, o, f, c) {
  var v = (o & ci) !== 0, d = (o & hi) === 0, h = v ? d ? /* @__PURE__ */ Ar(r, !1, !1) : dt(r) : r, p = (o & di) === 0 ? a : dt(a), w = {
    i: p,
    v: h,
    k: s,
    a: null,
    // @ts-expect-error
    e: null,
    prev: n,
    next: i
  };
  try {
    if (e === null) {
      var b = document.createDocumentFragment();
      b.append(e = ke());
    }
    return w.e = pe(() => l(
      /** @type {Node} */
      e,
      h,
      p,
      f
    ), y), w.e.prev = n && n.e, w.e.next = i && i.e, n === null ? c || (t.first = w) : (n.next = w, n.e.next = w.e), i !== null && (i.prev = w, i.e.prev = w.e), w;
  } finally {
  }
}
function bn(e, t, n) {
  for (var i = e.next ? (
    /** @type {TemplateNode} */
    e.next.e.nodes_start
  ) : n, r = t ? (
    /** @type {TemplateNode} */
    t.e.nodes_start
  ) : n, s = (
    /** @type {TemplateNode} */
    e.e.nodes_start
  ); s !== null && s !== i; ) {
    var a = (
      /** @type {TemplateNode} */
      /* @__PURE__ */ Re(s)
    );
    r.before(s), s = a;
  }
}
function Se(e, t, n) {
  t === null ? e.first = n : (t.next = n, t.e.next = n && n.e), n !== null && (n.prev = t, n.e.prev = t && t.e);
}
function Ts(e, t, n, i, r, s) {
  let a = y;
  y && qt();
  var l = null;
  y && x.nodeType === Si && (l = /** @type {Element} */
  x, qt());
  var o = (
    /** @type {TemplateNode} */
    y ? x : e
  ), f = new ni(o, !1);
  pn(() => {
    const c = t() || null;
    var v = c === "svg" ? gi : null;
    if (c === null) {
      f.ensure(null, null);
      return;
    }
    return f.ensure(c, (d) => {
      if (c) {
        if (l = y ? (
          /** @type {Element} */
          l
        ) : v ? document.createElementNS(v, c) : document.createElement(c), ut(l, l), i) {
          y && ws(c) && l.append(document.createComment(""));
          var h = (
            /** @type {TemplateNode} */
            y ? /* @__PURE__ */ Je(l) : l.appendChild(ke())
          );
          y && (h === null ? K(!1) : P(h)), i(l, h);
        }
        k.nodes_end = l, d.before(l);
      }
      y && P(d);
    }), () => {
    };
  }, Bt), zr(() => {
  }), a && (K(!0), P(o));
}
function ii(e, t) {
  Lr(() => {
    var n = e.getRootNode(), i = (
      /** @type {ShadowRoot} */
      n.host ? (
        /** @type {ShadowRoot} */
        n
      ) : (
        /** @type {Document} */
        n.head ?? /** @type {Document} */
        n.ownerDocument.head
      )
    );
    if (!i.querySelector("#" + t.hash)) {
      const r = document.createElement("style");
      r.id = t.hash, r.textContent = t.code, i.appendChild(r);
    }
  });
}
function Ss(e, t, n) {
  var i = e == null ? "" : "" + e;
  return t && (i = i ? i + " " + t : t), i === "" ? null : i;
}
function Cs(e, t) {
  return e == null ? null : String(e);
}
function be(e, t, n, i, r, s) {
  var a = e.__className;
  if (y || a !== n || a === void 0) {
    var l = Ss(n, i);
    (!y || l !== e.getAttribute("class")) && (l == null ? e.removeAttribute("class") : t ? e.className = l : e.setAttribute("class", l)), e.__className = n;
  }
  return s;
}
function He(e, t, n, i) {
  var r = e.__style;
  if (y || r !== t) {
    var s = Cs(t);
    (!y || s !== e.getAttribute("style")) && (s == null ? e.removeAttribute("style") : e.style.cssText = s), e.__style = t;
  }
  return i;
}
const qs = Symbol("is custom element"), As = Symbol("is html");
function si(e, t, n, i) {
  var r = Os(e);
  y && (r[t] = e.getAttribute(t), t === "src" || t === "srcset" || t === "href" && e.nodeName === "LINK") || r[t] !== (r[t] = n) && (t === "loading" && (e[Ti] = n), n == null ? e.removeAttribute(t) : typeof n != "string" && ai(e).includes(t) ? e[t] = n : e.setAttribute(t, n));
}
function or(e, t, n) {
  var i = E, r = k;
  let s = y;
  y && K(!1), V(null), ge(null);
  try {
    // `style` should use `set_attribute` rather than the setter
    t !== "style" && // Don't compute setters for custom elements while they aren't registered yet,
    // because during their upgrade/instantiation they might add more setters.
    // Instead, fall back to a simple "an object, then set as property" heuristic.
    (Rn.has(e.getAttribute("is") || e.nodeName) || // customElements may not be available in browser extension contexts
    !customElements || customElements.get(e.getAttribute("is") || e.tagName.toLowerCase()) ? ai(e).includes(t) : n && typeof n == "object") ? e[t] = n : si(e, t, n == null ? n : String(n));
  } finally {
    V(i), ge(r), s && K(!0);
  }
}
function Os(e) {
  return (
    /** @type {Record<string | symbol, unknown>} **/
    // @ts-expect-error
    e.__attributes ?? (e.__attributes = {
      [qs]: e.nodeName.includes("-"),
      [As]: e.namespaceURI === _i
    })
  );
}
var Rn = /* @__PURE__ */ new Map();
function ai(e) {
  var t = e.getAttribute("is") || e.nodeName, n = Rn.get(t);
  if (n) return n;
  Rn.set(t, n = []);
  for (var i, r = e, s = Element.prototype; s !== r; ) {
    i = wi(r);
    for (var a in i)
      i[a].set && n.push(a);
    r = hr(r);
  }
  return n;
}
function fr(e, t) {
  return e === t || (e == null ? void 0 : e[Ut]) === t;
}
function Ns(e = {}, t, n, i) {
  return Lr(() => {
    var r, s;
    return Wn(() => {
      r = s, s = [], Gn(() => {
        e !== n(...s) && (t(e, ...s), r && fr(n(...r), e) && t(null, ...r));
      });
    }), () => {
      dn(() => {
        s && fr(n(...s), e) && t(null, ...s);
      });
    };
  }), e;
}
function de(e, t, n, i) {
  var r = (
    /** @type {V} */
    i
  ), s = !0, a = () => (s && (s = !1, r = /** @type {V} */
  i), r), l;
  l = /** @type {V} */
  e[t], l === void 0 && i !== void 0 && (l = a());
  var o;
  o = () => {
    var d = (
      /** @type {V} */
      e[t]
    );
    return d === void 0 ? a() : (s = !0, d);
  };
  var f = !1, c = /* @__PURE__ */ vn(() => (f = !1, o())), v = (
    /** @type {Effect} */
    k
  );
  return (
    /** @type {() => V} */
    (function(d, h) {
      if (arguments.length > 0) {
        const p = h ? _(c) : d;
        return A(c, p), f = !0, r !== void 0 && (r = p), d;
      }
      return pt && f || (v.f & De) !== 0 ? c.v : _(c);
    })
  );
}
function Rs(e) {
  return new js(e);
}
var ze, ve;
class js {
  /**
   * @param {ComponentConstructorOptions & {
   *  component: any;
   * }} options
   */
  constructor(t) {
    /** @type {any} */
    C(this, ze);
    /** @type {Record<string, any>} */
    C(this, ve);
    var s;
    var n = /* @__PURE__ */ new Map(), i = (a, l) => {
      var o = /* @__PURE__ */ Ar(l, !1, !1);
      return n.set(a, o), o;
    };
    const r = new Proxy(
      { ...t.props || {}, $$events: {} },
      {
        get(a, l) {
          return _(n.get(l) ?? i(l, Reflect.get(a, l)));
        },
        has(a, l) {
          return l === ki ? !0 : (_(n.get(l) ?? i(l, Reflect.get(a, l))), Reflect.has(a, l));
        },
        set(a, l, o) {
          return A(n.get(l) ?? i(l, o), o), Reflect.set(a, l, o);
        }
      }
    );
    m(this, ve, (t.hydrate ? bs : ei)(t.component, {
      target: t.target,
      anchor: t.anchor,
      props: r,
      context: t.context,
      intro: t.intro ?? !1,
      recover: t.recover
    })), (!((s = t == null ? void 0 : t.props) != null && s.$$host) || t.sync === !1) && oe(), m(this, ze, r.$$events);
    for (const a of Object.keys(u(this, ve)))
      a === "$set" || a === "$destroy" || a === "$on" || Ct(this, a, {
        get() {
          return u(this, ve)[a];
        },
        /** @param {any} value */
        set(l) {
          u(this, ve)[a] = l;
        },
        enumerable: !0
      });
    u(this, ve).$set = /** @param {Record<string, any>} next */
    (a) => {
      Object.assign(r, a);
    }, u(this, ve).$destroy = () => {
      $s(u(this, ve));
    };
  }
  /** @param {Record<string, any>} props */
  $set(t) {
    u(this, ve).$set(t);
  }
  /**
   * @param {string} event
   * @param {(...args: any[]) => any} callback
   * @returns {any}
   */
  $on(t, n) {
    u(this, ze)[t] = u(this, ze)[t] || [];
    const i = (...r) => n.call(this, ...r);
    return u(this, ze)[t].push(i), () => {
      u(this, ze)[t] = u(this, ze)[t].filter(
        /** @param {any} fn */
        (r) => r !== i
      );
    };
  }
  $destroy() {
    u(this, ve).$destroy();
  }
}
ze = new WeakMap(), ve = new WeakMap();
let li;
typeof HTMLElement == "function" && (li = class extends HTMLElement {
  /**
   * @param {*} $$componentCtor
   * @param {*} $$slots
   * @param {*} use_shadow_dom
   */
  constructor(t, n, i) {
    super();
    /** The Svelte component constructor */
    M(this, "$$ctor");
    /** Slots */
    M(this, "$$s");
    /** @type {any} The Svelte component instance */
    M(this, "$$c");
    /** Whether or not the custom element is connected */
    M(this, "$$cn", !1);
    /** @type {Record<string, any>} Component props data */
    M(this, "$$d", {});
    /** `true` if currently in the process of reflecting component props back to attributes */
    M(this, "$$r", !1);
    /** @type {Record<string, CustomElementPropDefinition>} Props definition (name, reflected, type etc) */
    M(this, "$$p_d", {});
    /** @type {Record<string, EventListenerOrEventListenerObject[]>} Event listeners */
    M(this, "$$l", {});
    /** @type {Map<EventListenerOrEventListenerObject, Function>} Event listener unsubscribe functions */
    M(this, "$$l_u", /* @__PURE__ */ new Map());
    /** @type {any} The managed render effect for reflecting attributes */
    M(this, "$$me");
    this.$$ctor = t, this.$$s = n, i && this.attachShadow({ mode: "open" });
  }
  /**
   * @param {string} type
   * @param {EventListenerOrEventListenerObject} listener
   * @param {boolean | AddEventListenerOptions} [options]
   */
  addEventListener(t, n, i) {
    if (this.$$l[t] = this.$$l[t] || [], this.$$l[t].push(n), this.$$c) {
      const r = this.$$c.$on(t, n);
      this.$$l_u.set(n, r);
    }
    super.addEventListener(t, n, i);
  }
  /**
   * @param {string} type
   * @param {EventListenerOrEventListenerObject} listener
   * @param {boolean | AddEventListenerOptions} [options]
   */
  removeEventListener(t, n, i) {
    if (super.removeEventListener(t, n, i), this.$$c) {
      const r = this.$$l_u.get(n);
      r && (r(), this.$$l_u.delete(n));
    }
  }
  async connectedCallback() {
    if (this.$$cn = !0, !this.$$c) {
      let t = function(r) {
        return (s) => {
          const a = document.createElement("slot");
          r !== "default" && (a.name = r), Ie(s, a);
        };
      };
      if (await Promise.resolve(), !this.$$cn || this.$$c)
        return;
      const n = {}, i = Ms(this);
      for (const r of this.$$s)
        r in i && (r === "default" && !this.$$d.children ? (this.$$d.children = t(r), n.default = !0) : n[r] = t(r));
      for (const r of this.attributes) {
        const s = this.$$g_p(r.name);
        s in this.$$d || (this.$$d[s] = Jt(s, r.value, this.$$p_d, "toProp"));
      }
      for (const r in this.$$p_d)
        !(r in this.$$d) && this[r] !== void 0 && (this.$$d[r] = this[r], delete this[r]);
      this.$$c = Rs({
        component: this.$$ctor,
        target: this.shadowRoot || this,
        props: {
          ...this.$$d,
          $$slots: n,
          $$host: this
        }
      }), this.$$me = ss(() => {
        Wn(() => {
          var r;
          this.$$r = !0;
          for (const s of Zt(this.$$c)) {
            if (!((r = this.$$p_d[s]) != null && r.reflect)) continue;
            this.$$d[s] = this.$$c[s];
            const a = Jt(
              s,
              this.$$d[s],
              this.$$p_d,
              "toAttribute"
            );
            a == null ? this.removeAttribute(this.$$p_d[s].attribute || s) : this.setAttribute(this.$$p_d[s].attribute || s, a);
          }
          this.$$r = !1;
        });
      });
      for (const r in this.$$l)
        for (const s of this.$$l[r]) {
          const a = this.$$c.$on(r, s);
          this.$$l_u.set(s, a);
        }
      this.$$l = {};
    }
  }
  // We don't need this when working within Svelte code, but for compatibility of people using this outside of Svelte
  // and setting attributes through setAttribute etc, this is helpful
  /**
   * @param {string} attr
   * @param {string} _oldValue
   * @param {string} newValue
   */
  attributeChangedCallback(t, n, i) {
    var r;
    this.$$r || (t = this.$$g_p(t), this.$$d[t] = Jt(t, i, this.$$p_d, "toProp"), (r = this.$$c) == null || r.$set({ [t]: this.$$d[t] }));
  }
  disconnectedCallback() {
    this.$$cn = !1, Promise.resolve().then(() => {
      !this.$$cn && this.$$c && (this.$$c.$destroy(), this.$$me(), this.$$c = void 0);
    });
  }
  /**
   * @param {string} attribute_name
   */
  $$g_p(t) {
    return Zt(this.$$p_d).find(
      (n) => this.$$p_d[n].attribute === t || !this.$$p_d[n].attribute && n.toLowerCase() === t
    ) || t;
  }
});
function Jt(e, t, n, i) {
  var s;
  const r = (s = n[e]) == null ? void 0 : s.type;
  if (t = r === "Boolean" && typeof t != "boolean" ? t != null : t, !i || !n[e])
    return t;
  if (i === "toAttribute")
    switch (r) {
      case "Object":
      case "Array":
        return t == null ? null : JSON.stringify(t);
      case "Boolean":
        return t ? "" : null;
      case "Number":
        return t ?? null;
      default:
        return t;
    }
  else
    switch (r) {
      case "Object":
      case "Array":
        return t && JSON.parse(t);
      case "Boolean":
        return t;
      // conversion already handled above
      case "Number":
        return t != null ? +t : t;
      default:
        return t;
    }
}
function Ms(e) {
  const t = {};
  return e.childNodes.forEach((n) => {
    t[
      /** @type {Element} node */
      n.slot || "default"
    ] = !0;
  }), t;
}
function oi(e, t, n, i, r, s) {
  let a = class extends li {
    constructor() {
      super(e, n, r), this.$$p_d = t;
    }
    static get observedAttributes() {
      return Zt(t).map(
        (l) => (t[l].attribute || l).toLowerCase()
      );
    }
  };
  return Zt(t).forEach((l) => {
    Ct(a.prototype, l, {
      get() {
        return this.$$c && l in this.$$c ? this.$$c[l] : this.$$d[l];
      },
      set(o) {
        var v;
        o = Jt(l, o, t), this.$$d[l] = o;
        var f = this.$$c;
        if (f) {
          var c = (v = wt(f, l)) == null ? void 0 : v.get;
          c ? f[l] = o : f.$set({ [l]: o });
        }
      }
    });
  }), i.forEach((l) => {
    Ct(a.prototype, l, {
      get() {
        var o;
        return (o = this.$$c) == null ? void 0 : o[l];
      }
    });
  }), s && (a = s(a)), e.element = /** @type {any} */
  a, a;
}
var Is = /* @__PURE__ */ _t('<span class="loading svelte-lv9s7p">Loading...</span>'), Ps = /* @__PURE__ */ _t("<div><!> <!></div>");
const zs = {
  hash: "svelte-lv9s7p",
  code: `.loading.svelte-lv9s7p {padding:1em;display:block;}.animation.svelte-lv9s7p {hui-card {display:flex;flex-direction:column;}}.outer-container.animation.svelte-lv9s7p {transition:margin-bottom 0.35s ease;}.outer-container.animation.open.svelte-lv9s7p,
  .outer-container.animation.opening.svelte-lv9s7p {margin-bottom:inherit;}.outer-container.animation.close.svelte-lv9s7p,
  .outer-container.animation.closing.svelte-lv9s7p {margin-bottom:var(--expander-animation-height, -100%);}.outer-container.animation.opening.svelte-lv9s7p {
    animation: svelte-lv9s7p-fadeInOpacity 0.5s forwards ease;
    -webkit-animation: svelte-lv9s7p-fadeInOpacity 0.5s forwards ease;}.outer-container.animation.closing.svelte-lv9s7p {
      animation: svelte-lv9s7p-fadeOutOpacity 0.5s forwards ease;
      -webkit-animation: svelte-lv9s7p-fadeOutOpacity 0.5s forwards ease;}
  @keyframes svelte-lv9s7p-fadeInOpacity {
      0% {
          opacity: 0;
      }
      100% {
          opacity: 1;
      }
  }
  @-webkit-keyframes svelte-lv9s7p-fadeInOpacity {
      0% {
          opacity: 0;
      }
      100% {
          opacity: 1;
      }
  }
    @keyframes svelte-lv9s7p-fadeOutOpacity {
      0% {
          opacity: 1;
      }
      100% {
          opacity: 0;
      }
  }
  @-webkit-keyframes svelte-lv9s7p-fadeOutOpacity {
      0% {
          opacity: 1;
      }
      100% {
          opacity: 0;
      }
  }`
};
function jn(e, t) {
  Vn(t, !0), ii(e, zs);
  const n = de(t, "type", 7, "div"), i = de(t, "config"), r = de(t, "hass"), s = de(t, "preview"), a = de(t, "marginTop", 7, "0px"), l = de(t, "open"), o = de(t, "animation", 7, !0), f = de(t, "animationState"), c = de(t, "clearCardCss", 7, !1);
  let v = /* @__PURE__ */ U(void 0), d = /* @__PURE__ */ U(!0), h = /* @__PURE__ */ U(0);
  const p = JSON.parse(JSON.stringify(i()));
  Gt(() => {
    _(v) && (_(v).hass = r());
  }), Gt(() => {
    _(v) && (_(v).preview = s());
  }), Gt(() => {
    var g;
    _(v) && (p.disabled = !l(), (g = _(v)._element) == null || g.dispatchEvent(new CustomEvent("card-visibility-changed")));
  }), ri(async () => {
    const g = document.createElement("hui-card");
    g.hass = r(), g.preview = s(), p.disabled = !l(), g.config = p, g.load(), _(v) && (c() && (g.style.setProperty("--ha-card-background", "transparent"), g.style.setProperty("--ha-card-box-shadow", "none"), g.style.setProperty("--ha-card-border-color", "transparent"), g.style.setProperty("--ha-card-border-width", "0px"), g.style.setProperty("--ha-card-border-radius", "0px"), g.style.setProperty("--ha-card-backdrop-filter", "none")), o() && new ResizeObserver((Q) => {
      for (const I of Q)
        if (I.contentBoxSize) {
          const me = Array.isArray(I.contentBoxSize) ? I.contentBoxSize[0] : I.contentBoxSize;
          A(h, me.blockSize || _(h), !0);
        } else
          A(h, I.contentRect.height || _(h), !0);
    }).observe(g), _(v).replaceWith(g), A(v, g, !0), A(d, !1));
  });
  var w = {
    get type() {
      return n();
    },
    set type(g = "div") {
      n(g), oe();
    },
    get config() {
      return i();
    },
    set config(g) {
      i(g), oe();
    },
    get hass() {
      return r();
    },
    set hass(g) {
      r(g), oe();
    },
    get preview() {
      return s();
    },
    set preview(g) {
      s(g), oe();
    },
    get marginTop() {
      return a();
    },
    set marginTop(g = "0px") {
      a(g), oe();
    },
    get open() {
      return l();
    },
    set open(g) {
      l(g), oe();
    },
    get animation() {
      return o();
    },
    set animation(g = !0) {
      o(g), oe();
    },
    get animationState() {
      return f();
    },
    set animationState(g) {
      f(g), oe();
    },
    get clearCardCss() {
      return c();
    },
    set clearCardCss(g = !1) {
      c(g), oe();
    }
  }, b = Ps(), z = Ye(b);
  Ts(z, n, !1, (g, O) => {
    Ns(g, (Q) => A(v, Q, !0), () => _(v)), be(g, 0, "svelte-lv9s7p");
  });
  var N = Kt(z, 2);
  {
    var S = (g) => {
      var O = Is();
      Ie(g, O);
    };
    jt(N, (g) => {
      _(d) && g(S);
    });
  }
  return Me(b), Ve(() => {
    be(b, 1, `outer-container${l() ? " open" : " close"} ${f() ?? ""} ${o() ? "animation" : ""}`, "svelte-lv9s7p"), He(b, `margin-top: ${(l() ? a() : "0px") ?? ""};${_(h) ? ` --expander-animation-height: -${_(h)}px;` : ""}`);
  }), Ie(e, b), Hn(w);
}
customElements.define("expander-sub-card", oi(
  jn,
  {
    type: {},
    config: {},
    hass: {},
    preview: {},
    marginTop: {},
    open: {},
    animation: {},
    animationState: {},
    clearCardCss: {}
  },
  [],
  [],
  !0
));
const Mn = {
  gap: "0.0em",
  "expanded-gap": "0.6em",
  padding: "1em",
  clear: !1,
  "clear-children": !1,
  title: " ",
  "overlay-margin": "0.0em",
  "child-padding": "0.0em",
  "child-margin-top": "0.0em",
  "button-background": "transparent",
  "expander-card-background": "var(--ha-card-background,var(--card-background-color,#fff))",
  "header-color": "var(--primary-text-color,#fff)",
  "arrow-color": "var(--arrow-color,var(--primary-text-color,#fff))",
  "expander-card-display": "block",
  "title-card-clickable": !1,
  "min-width-expanded": 0,
  "max-width-expanded": 0,
  icon: "mdi:chevron-down",
  "icon-rotate-degree": "180deg",
  animation: !0
};
var Ds = /* @__PURE__ */ _t('<button aria-label="Toggle button"><ha-icon></ha-icon></button>', 2), Ls = /* @__PURE__ */ _t('<div id="id1"><div id="id2" class="title-card-container svelte-1jqiztq"><!></div> <!></div>'), Fs = /* @__PURE__ */ _t("<button><div> </div> <ha-icon></ha-icon></button>", 2), Bs = /* @__PURE__ */ _t("<div><div></div></div>"), Ys = /* @__PURE__ */ _t("<ha-card><!> <!></ha-card>", 2);
const Vs = {
  hash: "svelte-1jqiztq",
  code: `.expander-card.svelte-1jqiztq {display:var(--expander-card-display,block);gap:var(--gap);padding:var(--padding);background:var(--card-background,#fff);}.expander-card.animation.svelte-1jqiztq {transition:gap 0.35s ease;}.children-wrapper.svelte-1jqiztq {display:flex;flex-direction:column;}.children-wrapper.animation.opening.svelte-1jqiztq,
    .children-wrapper.animation.closing.svelte-1jqiztq {overflow:hidden;}.children-container.animation.svelte-1jqiztq {transition:padding 0.35s ease, gap 0.35s ease;}.children-container.svelte-1jqiztq {padding:var(--child-padding);display:var(--expander-card-display,block);gap:var(--gap);}.clear.svelte-1jqiztq {background:none !important;background-color:transparent !important;border-style:none !important;}.title-card-header.svelte-1jqiztq {display:flex;align-items:center;justify-content:space-between;flex-direction:row;}.title-card-header-overlay.svelte-1jqiztq {display:block;}.title-card-container.svelte-1jqiztq {width:100%;padding:var(--title-padding);}.header.svelte-1jqiztq {display:flex;flex-direction:row;align-items:center;padding:0.8em 0.8em;margin:2px;background:var(--button-background);border-style:none;width:var(--header-width,auto);color:var(--header-color,#fff);}.header-overlay.svelte-1jqiztq {position:absolute;top:0;right:0;margin:var(--overlay-margin);}.title.svelte-1jqiztq {width:100%;text-align:left;}.ico.animation.svelte-1jqiztq {transition-property:transform;transition-duration:0.35s;}.ico.svelte-1jqiztq {color:var(--arrow-color,var(--primary-text-color,#fff));}.flipped.svelte-1jqiztq {transform:rotate(var(--icon-rotate-degree,180deg));}.ripple.svelte-1jqiztq {background-position:center;transition:background 0.8s;border-radius:1em;}.ripple.svelte-1jqiztq:hover {background:#ffffff12 radial-gradient(circle, transparent 1%, #ffffff12 1%) center/15000%;}.ripple.svelte-1jqiztq:active {background-color:#ffffff25;background-size:100%;transition:background 0s;}`
};
function Hs(e, t) {
  var Jn, Zn;
  Vn(t, !0), ii(e, Vs);
  const n = de(t, "hass"), i = de(t, "preview"), r = de(t, "config", 7, Mn);
  let s = /* @__PURE__ */ U(!1), a = /* @__PURE__ */ U(!1), l = /* @__PURE__ */ U("idle"), o = /* @__PURE__ */ U(null);
  const f = r()["storage-id"] ?? r()["storgage-id"], c = "expander-open-" + f, v = r()["show-button-users"] === void 0 || ((Zn = r()["show-button-users"]) == null ? void 0 : Zn.includes((Jn = n()) == null ? void 0 : Jn.user.name));
  function d($) {
    _(o) && (clearTimeout(_(o)), A(o, null));
    const T = $ !== void 0 ? $ : !_(a);
    r().animation ? (A(l, T ? "opening" : "closing", !0), T ? (h(!0), A(
      o,
      setTimeout(
        () => {
          A(l, "idle"), A(o, null);
        },
        350
      ),
      !0
    )) : A(
      o,
      setTimeout(
        () => {
          h(!1), A(l, "idle"), A(o, null);
        },
        350
      ),
      !0
    )) : h(T);
  }
  function h($) {
    if (A(a, $, !0), f !== void 0)
      try {
        localStorage.setItem(c, _(a) ? "true" : "false");
      } catch (T) {
        console.error(T);
      }
  }
  function p($) {
    var q, ie;
    const T = (ie = (q = $.detail) == null ? void 0 : q["expander-card"]) == null ? void 0 : ie.data;
    (T == null ? void 0 : T["expander-card-id"]) === r()["expander-card-id"] && (T.action === "open" && !_(a) ? d(!0) : T.action === "close" && _(a) ? d(!1) : T.action === "toggle" && d());
  }
  function w() {
    document.body.removeEventListener("ll-custom", p);
  }
  ri(() => {
    var ie, we;
    const $ = r()["min-width-expanded"], T = r()["max-width-expanded"], q = document.body.offsetWidth;
    if ($ && T ? r().expanded = q >= $ && q <= T : $ ? r().expanded = q >= $ : T && (r().expanded = q <= T), (we = r()["start-expanded-users"]) != null && we.includes((ie = n()) == null ? void 0 : ie.user.name))
      h(!0);
    else if (f !== void 0)
      try {
        const B = localStorage.getItem(c);
        B === null ? r().expanded !== void 0 && h(r().expanded) : A(a, B ? B === "true" : _(a), !0);
      } catch (B) {
        console.error(B);
      }
    else
      r().expanded !== void 0 && h(r().expanded);
    return document.body.addEventListener("ll-custom", p), w;
  });
  const b = ($) => {
    if (_(s))
      return $.preventDefault(), $.stopImmediatePropagation(), A(s, !1), !1;
    d();
  }, z = ($) => {
    const T = $.currentTarget;
    T != null && T.classList.contains("title-card-container") && b($);
  };
  let N, S = !1, g = 0, O = 0;
  const Q = ($) => {
    N = $.target, g = $.touches[0].clientX, O = $.touches[0].clientY, S = !1;
  }, I = ($) => {
    const T = $.touches[0].clientX, q = $.touches[0].clientY;
    (Math.abs(T - g) > 10 || Math.abs(q - O) > 10) && (S = !0);
  }, me = ($) => {
    !S && N === $.target && r()["title-card-clickable"] && d(), N = void 0, A(s, !0);
  };
  var re = {
    get hass() {
      return n();
    },
    set hass($) {
      n($), oe();
    },
    get preview() {
      return i();
    },
    set preview($) {
      i($), oe();
    },
    get config() {
      return r();
    },
    set config($ = Mn) {
      r($), oe();
    }
  }, Te = Ys(), Be = Ye(Te);
  {
    var et = ($) => {
      var T = Ls(), q = Ye(T);
      q.__touchstart = Q, q.__touchmove = I, q.__touchend = me, q.__click = function(...ee) {
        var se;
        (se = r()["title-card-clickable"] ? z : null) == null || se.apply(this, ee);
      };
      var ie = Ye(q);
      {
        let ee = /* @__PURE__ */ Vt(() => r()["clear-children"] || !1);
        jn(ie, {
          get hass() {
            return n();
          },
          get preview() {
            return i();
          },
          get config() {
            return r()["title-card"];
          },
          get type() {
            return r()["title-card"].type;
          },
          animation: !1,
          open: !0,
          animationState: "idle",
          get clearCardCss() {
            return _(ee);
          }
        });
      }
      Me(q);
      var we = Kt(q, 2);
      {
        var B = (ee) => {
          var se = Ds();
          se.__click = b;
          var tt = Ye(se);
          Ve(() => or(tt, "icon", r().icon)), Me(se), Ve(() => {
            He(se, `--overlay-margin:${r()["overlay-margin"] ?? ""}; --button-background:${r()["button-background"] ?? ""}; --header-color:${r()["header-color"] ?? ""};`), be(se, 1, `header ripple${r()["title-card-button-overlay"] ? " header-overlay" : ""}${_(a) ? " open" : " close"}`, "svelte-1jqiztq"), He(tt, `--arrow-color:${r()["arrow-color"] ?? ""}`), be(tt, 1, `ico${_(a) && _(l) !== "closing" ? " flipped open" : " close"} ${r().animation ? "animation" : ""}`, "svelte-1jqiztq");
          }), Ie(ee, se);
        };
        jt(we, (ee) => {
          v && ee(B);
        });
      }
      Me(T), Ve(() => {
        be(T, 1, `title-card-header${r()["title-card-button-overlay"] ? "-overlay" : ""}`, "svelte-1jqiztq"), He(q, `--title-padding:${r()["title-card-padding"] ?? ""}`), si(q, "role", r()["title-card-clickable"] ? "button" : void 0);
      }), Ie($, T);
    }, gn = ($) => {
      var T = ps(), q = ts(T);
      {
        var ie = (we) => {
          var B = Fs();
          B.__click = b;
          var ee = Ye(B), se = Ye(ee, !0);
          Me(ee);
          var tt = Kt(ee, 2);
          Ve(() => or(tt, "icon", r().icon)), Me(B), Ve(() => {
            be(B, 1, `header${r()["expander-card-background-expanded"] ? "" : " ripple"}${_(a) ? " open" : " close"}`, "svelte-1jqiztq"), He(B, `--header-width:100%; --button-background:${r()["button-background"] ?? ""};--header-color:${r()["header-color"] ?? ""};`), be(ee, 1, `primary title${_(a) ? " open" : " close"}`, "svelte-1jqiztq"), ys(se, r().title), He(tt, `--arrow-color:${r()["arrow-color"] ?? ""}`), be(tt, 1, `ico${_(a) && _(l) !== "closing" ? " flipped open" : " close"} ${r().animation ? "animation" : ""}`, "svelte-1jqiztq");
          }), Ie(we, B);
        };
        jt(q, (we) => {
          v && we(ie);
        });
      }
      Ie($, T);
    };
    jt(Be, ($) => {
      r()["title-card"] ? $(et) : $(gn, !1);
    });
  }
  var mn = Kt(Be, 2);
  {
    var wn = ($) => {
      var T = Bs(), q = Ye(T);
      xs(q, 20, () => r().cards, (ie) => ie, (ie, we) => {
        {
          let B = /* @__PURE__ */ Vt(() => _(a) && i()), ee = /* @__PURE__ */ Vt(() => r().animation || !1), se = /* @__PURE__ */ Vt(() => r()["clear-children"] || !1);
          jn(ie, {
            get hass() {
              return n();
            },
            get preview() {
              return _(B);
            },
            get config() {
              return we;
            },
            get type() {
              return we.type;
            },
            get marginTop() {
              return r()["child-margin-top"];
            },
            get open() {
              return _(a);
            },
            get animation() {
              return _(ee);
            },
            get animationState() {
              return _(l);
            },
            get clearCardCss() {
              return _(se);
            }
          });
        }
      }), Me(q), Me(T), Ve(() => {
        be(T, 1, `children-wrapper ${r().animation ? "animation " + _(l) : ""}`, "svelte-1jqiztq"), He(q, `--expander-card-display:${r()["expander-card-display"] ?? ""};
                --gap:${(_(a) && _(l) !== "closing" ? r()["expanded-gap"] : r().gap) ?? ""};
                --child-padding:${(_(a) && _(l) !== "closing" ? r()["child-padding"] : "0px") ?? ""};`), be(q, 1, `children-container${_(a) ? " open" : " close"} ${_(l) ?? ""} ${r().animation ? "animation" : ""}`, "svelte-1jqiztq");
      }), Ie($, T);
    };
    jt(mn, ($) => {
      r().cards && $(wn);
    });
  }
  return Me(Te), Ve(() => {
    be(Te, 1, `expander-card${r().clear ? " clear" : ""}${_(a) ? " open" : " close"} ${_(l)} ${r().animation ? "animation" : ""}`, "svelte-1jqiztq"), He(Te, `--expander-card-display:${r()["expander-card-display"] ?? ""};
     --gap:${(_(a) && _(l) !== "closing" ? r()["expanded-gap"] : r().gap) ?? ""}; --padding:${r().padding ?? ""};
     --expander-state:${_(a) ?? ""};
     --icon-rotate-degree:${r()["icon-rotate-degree"] ?? ""};
     --card-background:${(_(a) && r()["expander-card-background-expanded"] ? r()["expander-card-background-expanded"] : r()["expander-card-background"]) ?? ""}
    `);
  }), Ie(e, Te), Hn(re);
}
hs(["touchstart", "touchmove", "touchend", "click"]);
customElements.define("expander-card", oi(Hs, { hass: {}, preview: {}, config: {} }, [], [], !0, (e) => class extends e {
  constructor() {
    super(...arguments);
    // re-declare props used in customClass.
    M(this, "config");
  }
  setConfig(n = {}) {
    this.config = { ...Mn, ...n };
  }
}));
const Us = "2.10.0";
console.info(
  `%c  Expander-Card 
%c Version ${Us}`,
  "color: orange; font-weight: bold; background: black",
  "color: white; font-weight: bold; background: dimgray"
);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "expander-card",
  name: "Expander Card",
  preview: !0,
  description: "Expander card"
});
export {
  Hs as default
};
//# sourceMappingURL=expander-card.js.map
