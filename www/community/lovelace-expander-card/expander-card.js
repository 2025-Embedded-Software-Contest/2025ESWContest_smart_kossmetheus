var Qr = Object.defineProperty;
var Wn = (e) => {
  throw TypeError(e);
};
var ei = (e, t, n) => t in e ? Qr(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var M = (e, t, n) => ei(e, typeof t != "symbol" ? t + "" : t, n), _n = (e, t, n) => t.has(e) || Wn("Cannot " + n);
var u = (e, t, n) => (_n(e, t, "read from private field"), n ? n.call(e) : t.get(e)), S = (e, t, n) => t.has(e) ? Wn("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, n), w = (e, t, n, i) => (_n(e, t, "write to private field"), i ? i.call(e, n) : t.set(e, n), n), P = (e, t, n) => (_n(e, t, "access private method"), n);
var ir;
typeof window < "u" && ((ir = window.__svelte ?? (window.__svelte = {})).v ?? (ir.v = /* @__PURE__ */ new Set())).add("5");
const ti = 1, ni = 2, ri = 16, ii = 1, si = 2, sr = "[", on = "[!", Nn = "]", Et = {}, z = Symbol(), ai = "http://www.w3.org/1999/xhtml", li = "http://www.w3.org/2000/svg", ar = !1;
var Rn = Array.isArray, oi = Array.prototype.indexOf, jn = Array.from, Zt = Object.keys, xt = Object.defineProperty, gt = Object.getOwnPropertyDescriptor, fi = Object.getOwnPropertyDescriptors, ui = Object.prototype, ci = Array.prototype, lr = Object.getPrototypeOf, Xn = Object.isExtensible;
function di(e) {
  for (var t = 0; t < e.length; t++)
    e[t]();
}
function or() {
  var e, t, n = new Promise((i, r) => {
    e = i, t = r;
  });
  return { promise: n, resolve: e, reject: t };
}
const J = 2, In = 4, Pn = 8, ft = 16, Pe = 32, Ue = 64, Mn = 128, he = 256, Qt = 512, W = 1024, oe = 2048, We = 4096, $e = 8192, ut = 16384, zn = 32768, Dt = 65536, Gn = 1 << 17, vi = 1 << 18, ct = 1 << 19, hi = 1 << 20, mn = 1 << 21, Dn = 1 << 22, rt = 1 << 23, Ht = Symbol("$state"), pi = Symbol("legacy props"), _i = Symbol(""), _t = new class extends Error {
  constructor() {
    super(...arguments);
    M(this, "name", "StaleReactionError");
    M(this, "message", "The reaction that called `getAbortSignal()` was re-run or destroyed");
  }
}(), gi = 1, Ln = 3, Ct = 8;
function mi(e) {
  throw new Error("https://svelte.dev/e/lifecycle_outside_component");
}
function yi() {
  throw new Error("https://svelte.dev/e/async_derived_orphan");
}
function wi(e) {
  throw new Error("https://svelte.dev/e/effect_in_teardown");
}
function $i() {
  throw new Error("https://svelte.dev/e/effect_in_unowned_derived");
}
function bi(e) {
  throw new Error("https://svelte.dev/e/effect_orphan");
}
function Ei() {
  throw new Error("https://svelte.dev/e/effect_update_depth_exceeded");
}
function xi() {
  throw new Error("https://svelte.dev/e/hydration_failed");
}
function ki() {
  throw new Error("https://svelte.dev/e/state_descriptors_fixed");
}
function Ti() {
  throw new Error("https://svelte.dev/e/state_prototype_fixed");
}
function Si() {
  throw new Error("https://svelte.dev/e/state_unsafe_mutation");
}
function Ci() {
  throw new Error("https://svelte.dev/e/svelte_boundary_reset_onerror");
}
function fn(e) {
  console.warn("https://svelte.dev/e/hydration_mismatch");
}
function qi() {
  console.warn("https://svelte.dev/e/svelte_boundary_reset_noop");
}
let $ = !1;
function X(e) {
  $ = e;
}
let x;
function L(e) {
  if (e === null)
    throw fn(), Et;
  return x = e;
}
function kt() {
  return L(
    /** @type {TemplateNode} */
    /* @__PURE__ */ Oe(x)
  );
}
function Ne(e) {
  if ($) {
    if (/* @__PURE__ */ Oe(x) !== null)
      throw fn(), Et;
    x = e;
  }
}
function Oi(e = 1) {
  if ($) {
    for (var t = e, n = x; t--; )
      n = /** @type {TemplateNode} */
      /* @__PURE__ */ Oe(n);
    x = n;
  }
}
function en(e = !0) {
  for (var t = 0, n = x; ; ) {
    if (n.nodeType === Ct) {
      var i = (
        /** @type {Comment} */
        n.data
      );
      if (i === Nn) {
        if (t === 0) return n;
        t -= 1;
      } else (i === sr || i === on) && (t += 1);
    }
    var r = (
      /** @type {TemplateNode} */
      /* @__PURE__ */ Oe(n)
    );
    e && n.remove(), n = r;
  }
}
function fr(e) {
  if (!e || e.nodeType !== Ct)
    throw fn(), Et;
  return (
    /** @type {Comment} */
    e.data
  );
}
function ur(e) {
  return e === this.v;
}
function Ai(e, t) {
  return e != e ? t == t : e !== t || e !== null && typeof e == "object" || typeof e == "function";
}
function cr(e) {
  return !Ai(e, this.v);
}
let Ni = !1, fe = null;
function Tt(e) {
  fe = e;
}
function Fn(e, t = !1, n) {
  fe = {
    p: fe,
    c: null,
    e: null,
    s: e,
    x: null,
    l: null
  };
}
function Bn(e) {
  var t = (
    /** @type {ComponentContext} */
    fe
  ), n = t.e;
  if (n !== null) {
    t.e = null;
    for (var i of n)
      Ar(i);
  }
  return e !== void 0 && (t.x = e), fe = t.p, e ?? /** @type {T} */
  {};
}
function dr() {
  return !0;
}
let Je = [];
function vr() {
  var e = Je;
  Je = [], di(e);
}
function Rt(e) {
  if (Je.length === 0 && !At) {
    var t = Je;
    queueMicrotask(() => {
      t === Je && vr();
    });
  }
  Je.push(e);
}
function Ri() {
  for (; Je.length > 0; )
    vr();
}
const ji = /* @__PURE__ */ new WeakMap();
function hr(e) {
  var t = k;
  if (t === null)
    return E.f |= rt, e;
  if ((t.f & zn) === 0) {
    if ((t.f & Mn) === 0)
      throw !t.parent && e instanceof Error && pr(e), e;
    t.b.error(e);
  } else
    St(e, t);
}
function St(e, t) {
  for (; t !== null; ) {
    if ((t.f & Mn) !== 0)
      try {
        t.b.error(e);
        return;
      } catch (n) {
        e = n;
      }
    t = t.parent;
  }
  throw e instanceof Error && pr(e), e;
}
function pr(e) {
  const t = ji.get(e);
  t && (xt(e, "message", {
    value: t.message
  }), xt(e, "stack", {
    value: t.stack
  }));
}
const Bt = /* @__PURE__ */ new Set();
let j = null, D = null, yn = /* @__PURE__ */ new Set(), Se = [], un = null, wn = !1, At = !1;
var yt, wt, Ze, It, $t, Qe, bt, Pt, Mt, pe, $n, Ut, bn;
const sn = class sn {
  constructor() {
    S(this, pe);
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
    S(this, yt, /* @__PURE__ */ new Map());
    /**
     * When the batch is committed (and the DOM is updated), we need to remove old branches
     * and append new ones by calling the functions added inside (if/each/key/etc) blocks
     * @type {Set<() => void>}
     */
    S(this, wt, /* @__PURE__ */ new Set());
    /**
     * The number of async effects that are currently in flight
     */
    S(this, Ze, 0);
    /**
     * A deferred that resolves when the batch is committed, used with `settled()`
     * TODO replace with Promise.withResolvers once supported widely enough
     * @type {{ promise: Promise<void>, resolve: (value?: any) => void, reject: (reason: unknown) => void } | null}
     */
    S(this, It, null);
    /**
     * Template effects and `$effect.pre` effects, which run when
     * a batch is committed
     * @type {Effect[]}
     */
    S(this, $t, []);
    /**
     * The same as `#render_effects`, but for `$effect` (which runs after)
     * @type {Effect[]}
     */
    S(this, Qe, []);
    /**
     * Block effects, which may need to re-run on subsequent flushes
     * in order to update internal sources (e.g. each block items)
     * @type {Effect[]}
     */
    S(this, bt, []);
    /**
     * Deferred effects (which run after async work has completed) that are DIRTY
     * @type {Effect[]}
     */
    S(this, Pt, []);
    /**
     * Deferred effects that are MAYBE_DIRTY
     * @type {Effect[]}
     */
    S(this, Mt, []);
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
    var s;
    Se = [], this.apply();
    for (const a of t)
      P(this, pe, $n).call(this, a);
    if (u(this, Ze) === 0) {
      var n = D;
      P(this, pe, bn).call(this);
      var i = u(this, $t), r = u(this, Qe);
      w(this, $t, []), w(this, Qe, []), w(this, bt, []), j = null, D = n, Kn(i), Kn(r), (s = u(this, It)) == null || s.resolve();
    } else
      P(this, pe, Ut).call(this, u(this, $t)), P(this, pe, Ut).call(this, u(this, Qe)), P(this, pe, Ut).call(this, u(this, bt));
    D = null;
  }
  /**
   * Associate a change to a given source with the current
   * batch, noting its previous and current values
   * @param {Source} source
   * @param {any} value
   */
  capture(t, n) {
    u(this, yt).has(t) || u(this, yt).set(t, n), this.current.set(t, t.v), D == null || D.set(t, t.v);
  }
  activate() {
    j = this;
  }
  deactivate() {
    j = null, D = null;
  }
  flush() {
    if (Se.length > 0) {
      if (this.activate(), _r(), j !== null && j !== this)
        return;
    } else u(this, Ze) === 0 && P(this, pe, bn).call(this);
    this.deactivate();
    for (const t of yn)
      if (yn.delete(t), t(), j !== null)
        break;
  }
  increment() {
    w(this, Ze, u(this, Ze) + 1);
  }
  decrement() {
    w(this, Ze, u(this, Ze) - 1);
    for (const t of u(this, Pt))
      K(t, oe), lt(t);
    for (const t of u(this, Mt))
      K(t, We), lt(t);
    this.flush();
  }
  /** @param {() => void} fn */
  add_callback(t) {
    u(this, wt).add(t);
  }
  settled() {
    return (u(this, It) ?? w(this, It, or())).promise;
  }
  static ensure() {
    if (j === null) {
      const t = j = new sn();
      Bt.add(j), At || sn.enqueue(() => {
        j === t && t.flush();
      });
    }
    return j;
  }
  /** @param {() => void} task */
  static enqueue(t) {
    Rt(t);
  }
  apply() {
  }
};
yt = new WeakMap(), wt = new WeakMap(), Ze = new WeakMap(), It = new WeakMap(), $t = new WeakMap(), Qe = new WeakMap(), bt = new WeakMap(), Pt = new WeakMap(), Mt = new WeakMap(), pe = new WeakSet(), /**
 * Traverse the effect tree, executing effects or stashing
 * them for later execution as appropriate
 * @param {Effect} root
 */
$n = function(t) {
  t.f ^= W;
  for (var n = t.first; n !== null; ) {
    var i = n.f, r = (i & (Pe | Ue)) !== 0, s = r && (i & W) !== 0, a = s || (i & $e) !== 0 || this.skipped_effects.has(n);
    if (!a && n.fn !== null) {
      r ? n.f ^= W : (i & In) !== 0 ? u(this, Qe).push(n) : hn(n) && ((n.f & ft) !== 0 && u(this, bt).push(n), rn(n));
      var l = n.first;
      if (l !== null) {
        n = l;
        continue;
      }
    }
    var o = n.parent;
    for (n = n.next; n === null && o !== null; )
      n = o.next, o = o.parent;
  }
}, /**
 * @param {Effect[]} effects
 */
Ut = function(t) {
  for (const n of t)
    ((n.f & oe) !== 0 ? u(this, Pt) : u(this, Mt)).push(n), K(n, W);
  t.length = 0;
}, /**
 * Append and remove branches to/from the DOM
 */
bn = function() {
  var t;
  for (const n of u(this, wt))
    n();
  if (u(this, wt).clear(), Bt.size > 1) {
    u(this, yt).clear();
    let n = !0;
    for (const i of Bt) {
      if (i === this) {
        n = !1;
        continue;
      }
      const r = [];
      for (const [a, l] of this.current) {
        if (i.current.has(a))
          if (n && l !== i.current.get(a))
            i.current.set(a, l);
          else
            continue;
        r.push(a);
      }
      if (r.length === 0)
        continue;
      const s = [...i.current.keys()].filter((a) => !this.current.has(a));
      if (s.length > 0) {
        for (const a of r)
          gr(a, s);
        if (Se.length > 0) {
          j = i, i.apply();
          for (const a of Se)
            P(t = i, pe, $n).call(t, a);
          Se = [], i.deactivate();
        }
      }
    }
    j = null;
  }
  Bt.delete(this);
};
let Ce = sn;
function ae(e) {
  var t = At;
  At = !0;
  try {
    for (var n; ; ) {
      if (Ri(), Se.length === 0 && (j == null || j.flush(), Se.length === 0))
        return un = null, /** @type {T} */
        n;
      _r();
    }
  } finally {
    At = t;
  }
}
function _r() {
  var e = mt;
  wn = !0;
  try {
    var t = 0;
    for (Zn(!0); Se.length > 0; ) {
      var n = Ce.ensure();
      if (t++ > 1e3) {
        var i, r;
        Ii();
      }
      n.process(Se), Ve.clear();
    }
  } finally {
    wn = !1, Zn(e), un = null;
  }
}
function Ii() {
  try {
    Ei();
  } catch (e) {
    St(e, un);
  }
}
let Re = null;
function Kn(e) {
  var t = e.length;
  if (t !== 0) {
    for (var n = 0; n < t; ) {
      var i = e[n++];
      if ((i.f & (ut | $e)) === 0 && hn(i) && (Re = [], rn(i), i.deps === null && i.first === null && i.nodes_start === null && (i.teardown === null && i.ac === null ? Ir(i) : i.fn = null), (Re == null ? void 0 : Re.length) > 0)) {
        Ve.clear();
        for (const r of Re)
          rn(r);
        Re = [];
      }
    }
    Re = null;
  }
}
function gr(e, t) {
  if (e.reactions !== null)
    for (const n of e.reactions) {
      const i = n.f;
      (i & J) !== 0 ? gr(
        /** @type {Derived} */
        n,
        t
      ) : (i & (Dn | ft)) !== 0 && mr(n, t) && (K(n, oe), lt(
        /** @type {Effect} */
        n
      ));
    }
}
function mr(e, t) {
  if (e.deps !== null) {
    for (const n of e.deps)
      if (t.includes(n) || (n.f & J) !== 0 && mr(
        /** @type {Derived} */
        n,
        t
      ))
        return !0;
  }
  return !1;
}
function lt(e) {
  for (var t = un = e; t.parent !== null; ) {
    t = t.parent;
    var n = t.f;
    if (wn && t === k && (n & ft) !== 0)
      return;
    if ((n & (Ue | Pe)) !== 0) {
      if ((n & W) === 0) return;
      t.f ^= W;
    }
  }
  Se.push(t);
}
function Pi(e) {
  let t = 0, n = ot(0), i;
  return () => {
    Gi() && (g(n), Vn(() => (t === 0 && (i = Un(() => e(() => Nt(n)))), t += 1, () => {
      Rt(() => {
        t -= 1, t === 0 && (i == null || i(), i = void 0, Nt(n));
      });
    })));
  };
}
var Mi = Dt | ct | Mn;
function zi(e, t, n) {
  new Di(e, t, n);
}
var ye, se, zt, xe, et, ke, de, te, Te, Le, tt, Fe, nt, Be, an, ln, F, yr, wr, Wt, Xt, En;
class Di {
  /**
   * @param {TemplateNode} node
   * @param {BoundaryProps} props
   * @param {((anchor: Node) => void)} children
   */
  constructor(t, n, i) {
    S(this, F);
    /** @type {Boundary | null} */
    M(this, "parent");
    S(this, ye, !1);
    /** @type {TemplateNode} */
    S(this, se);
    /** @type {TemplateNode | null} */
    S(this, zt, $ ? x : null);
    /** @type {BoundaryProps} */
    S(this, xe);
    /** @type {((anchor: Node) => void)} */
    S(this, et);
    /** @type {Effect} */
    S(this, ke);
    /** @type {Effect | null} */
    S(this, de, null);
    /** @type {Effect | null} */
    S(this, te, null);
    /** @type {Effect | null} */
    S(this, Te, null);
    /** @type {DocumentFragment | null} */
    S(this, Le, null);
    S(this, tt, 0);
    S(this, Fe, 0);
    S(this, nt, !1);
    /**
     * A source containing the number of pending async deriveds/expressions.
     * Only created if `$effect.pending()` is used inside the boundary,
     * otherwise updating the source results in needless `Batch.ensure()`
     * calls followed by no-op flushes
     * @type {Source<number> | null}
     */
    S(this, Be, null);
    S(this, an, () => {
      u(this, Be) && tn(u(this, Be), u(this, tt));
    });
    S(this, ln, Pi(() => (w(this, Be, ot(u(this, tt))), () => {
      w(this, Be, null);
    })));
    w(this, se, t), w(this, xe, n), w(this, et, i), this.parent = /** @type {Effect} */
    k.b, w(this, ye, !!u(this, xe).pending), w(this, ke, dn(() => {
      if (k.b = this, $) {
        const r = u(this, zt);
        kt(), /** @type {Comment} */
        r.nodeType === Ct && /** @type {Comment} */
        r.data === on ? P(this, F, wr).call(this) : P(this, F, yr).call(this);
      } else {
        try {
          w(this, de, le(() => i(u(this, se))));
        } catch (r) {
          this.error(r);
        }
        u(this, Fe) > 0 ? P(this, F, Xt).call(this) : w(this, ye, !1);
      }
    }, Mi)), $ && w(this, se, x);
  }
  /**
   * Returns `true` if the effect exists inside a boundary whose pending snippet is shown
   * @returns {boolean}
   */
  is_pending() {
    return u(this, ye) || !!this.parent && this.parent.is_pending();
  }
  has_pending_snippet() {
    return !!u(this, xe).pending;
  }
  /**
   * Update the source that powers `$effect.pending()` inside this boundary,
   * and controls when the current `pending` snippet (if any) is removed.
   * Do not call from inside the class
   * @param {1 | -1} d
   */
  update_pending_count(t) {
    P(this, F, En).call(this, t), w(this, tt, u(this, tt) + t), yn.add(u(this, an));
  }
  get_effect_pending() {
    return u(this, ln).call(this), g(
      /** @type {Source<number>} */
      u(this, Be)
    );
  }
  /** @param {unknown} error */
  error(t) {
    var n = u(this, xe).onerror;
    let i = u(this, xe).failed;
    if (u(this, nt) || !n && !i)
      throw t;
    u(this, de) && (ne(u(this, de)), w(this, de, null)), u(this, te) && (ne(u(this, te)), w(this, te, null)), u(this, Te) && (ne(u(this, Te)), w(this, Te, null)), $ && (L(
      /** @type {TemplateNode} */
      u(this, zt)
    ), Oi(), L(en()));
    var r = !1, s = !1;
    const a = () => {
      if (r) {
        qi();
        return;
      }
      r = !0, s && Ci(), Ce.ensure(), w(this, tt, 0), u(this, Te) !== null && it(u(this, Te), () => {
        w(this, Te, null);
      }), w(this, ye, this.has_pending_snippet()), w(this, de, P(this, F, Wt).call(this, () => (w(this, nt, !1), le(() => u(this, et).call(this, u(this, se)))))), u(this, Fe) > 0 ? P(this, F, Xt).call(this) : w(this, ye, !1);
    };
    var l = E;
    try {
      Y(null), s = !0, n == null || n(t, a), s = !1;
    } catch (o) {
      St(o, u(this, ke) && u(this, ke).parent);
    } finally {
      Y(l);
    }
    i && Rt(() => {
      w(this, Te, P(this, F, Wt).call(this, () => {
        w(this, nt, !0);
        try {
          return le(() => {
            i(
              u(this, se),
              () => t,
              () => a
            );
          });
        } catch (o) {
          return St(
            o,
            /** @type {Effect} */
            u(this, ke).parent
          ), null;
        } finally {
          w(this, nt, !1);
        }
      }));
    });
  }
}
ye = new WeakMap(), se = new WeakMap(), zt = new WeakMap(), xe = new WeakMap(), et = new WeakMap(), ke = new WeakMap(), de = new WeakMap(), te = new WeakMap(), Te = new WeakMap(), Le = new WeakMap(), tt = new WeakMap(), Fe = new WeakMap(), nt = new WeakMap(), Be = new WeakMap(), an = new WeakMap(), ln = new WeakMap(), F = new WeakSet(), yr = function() {
  try {
    w(this, de, le(() => u(this, et).call(this, u(this, se))));
  } catch (t) {
    this.error(t);
  }
  w(this, ye, !1);
}, wr = function() {
  const t = u(this, xe).pending;
  t && (w(this, te, le(() => t(u(this, se)))), Ce.enqueue(() => {
    w(this, de, P(this, F, Wt).call(this, () => (Ce.ensure(), le(() => u(this, et).call(this, u(this, se)))))), u(this, Fe) > 0 ? P(this, F, Xt).call(this) : (it(
      /** @type {Effect} */
      u(this, te),
      () => {
        w(this, te, null);
      }
    ), w(this, ye, !1));
  }));
}, /**
 * @param {() => Effect | null} fn
 */
Wt = function(t) {
  var n = k, i = E, r = fe;
  _e(u(this, ke)), Y(u(this, ke)), Tt(u(this, ke).ctx);
  try {
    return t();
  } catch (s) {
    return hr(s), null;
  } finally {
    _e(n), Y(i), Tt(r);
  }
}, Xt = function() {
  const t = (
    /** @type {(anchor: Node) => void} */
    u(this, xe).pending
  );
  u(this, de) !== null && (w(this, Le, document.createDocumentFragment()), Li(u(this, de), u(this, Le))), u(this, te) === null && w(this, te, le(() => t(u(this, se))));
}, /**
 * Updates the pending count associated with the currently visible pending snippet,
 * if any, such that we can replace the snippet with content once work is done
 * @param {1 | -1} d
 */
En = function(t) {
  var n;
  if (!this.has_pending_snippet()) {
    this.parent && P(n = this.parent, F, En).call(n, t);
    return;
  }
  w(this, Fe, u(this, Fe) + t), u(this, Fe) === 0 && (w(this, ye, !1), u(this, te) && it(u(this, te), () => {
    w(this, te, null);
  }), u(this, Le) && (u(this, se).before(u(this, Le)), w(this, Le, null)), Rt(() => {
    Ce.ensure().flush();
  }));
};
function Li(e, t) {
  for (var n = e.nodes_start, i = e.nodes_end; n !== null; ) {
    var r = n === i ? null : (
      /** @type {TemplateNode} */
      /* @__PURE__ */ Oe(n)
    );
    t.append(n), n = r;
  }
}
function Fi(e, t, n) {
  const i = cn;
  if (t.length === 0) {
    n(e.map(i));
    return;
  }
  var r = j, s = (
    /** @type {Effect} */
    k
  ), a = Bi(), l = $;
  Promise.all(t.map((o) => /* @__PURE__ */ Yi(o))).then((o) => {
    a();
    try {
      n([...e.map(i), ...o]);
    } catch (f) {
      (s.f & ut) === 0 && St(f, s);
    }
    l && X(!1), r == null || r.deactivate(), xn();
  }).catch((o) => {
    St(o, s);
  });
}
function Bi() {
  var e = k, t = E, n = fe, i = j, r = $;
  if (r)
    var s = x;
  return function() {
    _e(e), Y(t), Tt(n), i == null || i.activate(), r && (X(!0), L(s));
  };
}
function xn() {
  _e(null), Y(null), Tt(null);
}
// @__NO_SIDE_EFFECTS__
function cn(e) {
  var t = J | oe, n = E !== null && (E.f & J) !== 0 ? (
    /** @type {Derived} */
    E
  ) : null;
  return k === null || n !== null && (n.f & he) !== 0 ? t |= he : k.f |= ct, {
    ctx: fe,
    deps: null,
    effects: null,
    equals: ur,
    f: t,
    fn: e,
    reactions: null,
    rv: 0,
    v: (
      /** @type {V} */
      z
    ),
    wv: 0,
    parent: n ?? k,
    ac: null
  };
}
// @__NO_SIDE_EFFECTS__
function Yi(e, t) {
  let n = (
    /** @type {Effect | null} */
    k
  );
  n === null && yi();
  var i = (
    /** @type {Boundary} */
    n.b
  ), r = (
    /** @type {Promise<V>} */
    /** @type {unknown} */
    void 0
  ), s = ot(
    /** @type {V} */
    z
  ), a = !E, l = /* @__PURE__ */ new Map();
  return Qi(() => {
    var c;
    var o = or();
    r = o.promise;
    try {
      Promise.resolve(e()).then(o.resolve, o.reject).then(xn);
    } catch (d) {
      o.reject(d), xn();
    }
    var f = (
      /** @type {Batch} */
      j
    ), p = i.is_pending();
    a && (i.update_pending_count(1), p || (f.increment(), (c = l.get(f)) == null || c.reject(_t), l.delete(f), l.set(f, o)));
    const h = (d, v = void 0) => {
      if (p || f.activate(), v)
        v !== _t && (s.f |= rt, tn(s, v));
      else {
        (s.f & rt) !== 0 && (s.f ^= rt), tn(s, d);
        for (const [m, y] of l) {
          if (l.delete(m), m === f) break;
          y.reject(_t);
        }
      }
      a && (i.update_pending_count(-1), p || f.decrement());
    };
    o.promise.then(h, (d) => h(null, d || "unknown"));
  }), Ki(() => {
    for (const o of l.values())
      o.reject(_t);
  }), new Promise((o) => {
    function f(p) {
      function h() {
        p === r ? o(s) : f(r);
      }
      p.then(h, h);
    }
    f(r);
  });
}
// @__NO_SIDE_EFFECTS__
function Yt(e) {
  const t = /* @__PURE__ */ cn(e);
  return zr(t), t;
}
// @__NO_SIDE_EFFECTS__
function Vi(e) {
  const t = /* @__PURE__ */ cn(e);
  return t.equals = cr, t;
}
function $r(e) {
  var t = e.effects;
  if (t !== null) {
    e.effects = null;
    for (var n = 0; n < t.length; n += 1)
      ne(
        /** @type {Effect} */
        t[n]
      );
  }
}
function Hi(e) {
  for (var t = e.parent; t !== null; ) {
    if ((t.f & J) === 0)
      return (
        /** @type {Effect} */
        t
      );
    t = t.parent;
  }
  return null;
}
function Yn(e) {
  var t, n = k;
  _e(Hi(e));
  try {
    $r(e), t = Br(e);
  } finally {
    _e(n);
  }
  return t;
}
function br(e) {
  var t = Yn(e);
  if (e.equals(t) || (e.v = t, e.wv = Lr()), !dt)
    if (D !== null)
      D.set(e, e.v);
    else {
      var n = (Ye || (e.f & he) !== 0) && e.deps !== null ? We : W;
      K(e, n);
    }
}
const Ve = /* @__PURE__ */ new Map();
function ot(e, t) {
  var n = {
    f: 0,
    // TODO ideally we could skip this altogether, but it causes type errors
    v: e,
    reactions: null,
    equals: ur,
    rv: 0,
    wv: 0
  };
  return n;
}
// @__NO_SIDE_EFFECTS__
function H(e, t) {
  const n = ot(e);
  return zr(n), n;
}
// @__NO_SIDE_EFFECTS__
function Er(e, t = !1, n = !0) {
  const i = ot(e);
  return t || (i.equals = cr), i;
}
function O(e, t, n = !1) {
  E !== null && // since we are untracking the function inside `$inspect.with` we need to add this check
  // to ensure we error if state is set inside an inspect effect
  (!we || (E.f & Gn) !== 0) && dr() && (E.f & (J | ft | Dn | Gn)) !== 0 && !(G != null && G.includes(e)) && Si();
  let i = n ? qt(t) : t;
  return tn(e, i);
}
function tn(e, t) {
  if (!e.equals(t)) {
    var n = e.v;
    dt ? Ve.set(e, t) : Ve.set(e, n), e.v = t;
    var i = Ce.ensure();
    i.capture(e, n), (e.f & J) !== 0 && ((e.f & oe) !== 0 && Yn(
      /** @type {Derived} */
      e
    ), K(e, (e.f & he) === 0 ? W : We)), e.wv = Lr(), xr(e, oe), k !== null && (k.f & W) !== 0 && (k.f & (Pe | Ue)) === 0 && (ue === null ? ns([e]) : ue.push(e));
  }
  return t;
}
function Nt(e) {
  O(e, e.v + 1);
}
function xr(e, t) {
  var n = e.reactions;
  if (n !== null)
    for (var i = n.length, r = 0; r < i; r++) {
      var s = n[r], a = s.f, l = (a & oe) === 0;
      l && K(s, t), (a & J) !== 0 ? xr(
        /** @type {Derived} */
        s,
        We
      ) : l && ((a & ft) !== 0 && Re !== null && Re.push(
        /** @type {Effect} */
        s
      ), lt(
        /** @type {Effect} */
        s
      ));
    }
}
function qt(e) {
  if (typeof e != "object" || e === null || Ht in e)
    return e;
  const t = lr(e);
  if (t !== ui && t !== ci)
    return e;
  var n = /* @__PURE__ */ new Map(), i = Rn(e), r = /* @__PURE__ */ H(0), s = st, a = (l) => {
    if (st === s)
      return l();
    var o = E, f = st;
    Y(null), er(s);
    var p = l();
    return Y(o), er(f), p;
  };
  return i && n.set("length", /* @__PURE__ */ H(
    /** @type {any[]} */
    e.length
  )), new Proxy(
    /** @type {any} */
    e,
    {
      defineProperty(l, o, f) {
        (!("value" in f) || f.configurable === !1 || f.enumerable === !1 || f.writable === !1) && ki();
        var p = n.get(o);
        return p === void 0 ? p = a(() => {
          var h = /* @__PURE__ */ H(f.value);
          return n.set(o, h), h;
        }) : O(p, f.value, !0), !0;
      },
      deleteProperty(l, o) {
        var f = n.get(o);
        if (f === void 0) {
          if (o in l) {
            const p = a(() => /* @__PURE__ */ H(z));
            n.set(o, p), Nt(r);
          }
        } else
          O(f, z), Nt(r);
        return !0;
      },
      get(l, o, f) {
        var d;
        if (o === Ht)
          return e;
        var p = n.get(o), h = o in l;
        if (p === void 0 && (!h || (d = gt(l, o)) != null && d.writable) && (p = a(() => {
          var v = qt(h ? l[o] : z), m = /* @__PURE__ */ H(v);
          return m;
        }), n.set(o, p)), p !== void 0) {
          var c = g(p);
          return c === z ? void 0 : c;
        }
        return Reflect.get(l, o, f);
      },
      getOwnPropertyDescriptor(l, o) {
        var f = Reflect.getOwnPropertyDescriptor(l, o);
        if (f && "value" in f) {
          var p = n.get(o);
          p && (f.value = g(p));
        } else if (f === void 0) {
          var h = n.get(o), c = h == null ? void 0 : h.v;
          if (h !== void 0 && c !== z)
            return {
              enumerable: !0,
              configurable: !0,
              value: c,
              writable: !0
            };
        }
        return f;
      },
      has(l, o) {
        var c;
        if (o === Ht)
          return !0;
        var f = n.get(o), p = f !== void 0 && f.v !== z || Reflect.has(l, o);
        if (f !== void 0 || k !== null && (!p || (c = gt(l, o)) != null && c.writable)) {
          f === void 0 && (f = a(() => {
            var d = p ? qt(l[o]) : z, v = /* @__PURE__ */ H(d);
            return v;
          }), n.set(o, f));
          var h = g(f);
          if (h === z)
            return !1;
        }
        return p;
      },
      set(l, o, f, p) {
        var T;
        var h = n.get(o), c = o in l;
        if (i && o === "length")
          for (var d = f; d < /** @type {Source<number>} */
          h.v; d += 1) {
            var v = n.get(d + "");
            v !== void 0 ? O(v, z) : d in l && (v = a(() => /* @__PURE__ */ H(z)), n.set(d + "", v));
          }
        if (h === void 0)
          (!c || (T = gt(l, o)) != null && T.writable) && (h = a(() => /* @__PURE__ */ H(void 0)), O(h, qt(f)), n.set(o, h));
        else {
          c = h.v !== z;
          var m = a(() => qt(f));
          O(h, m);
        }
        var y = Reflect.getOwnPropertyDescriptor(l, o);
        if (y != null && y.set && y.set.call(p, f), !c) {
          if (i && typeof o == "string") {
            var N = (
              /** @type {Source<number>} */
              n.get("length")
            ), C = Number(o);
            Number.isInteger(C) && C >= N.v && O(N, C + 1);
          }
          Nt(r);
        }
        return !0;
      },
      ownKeys(l) {
        g(r);
        var o = Reflect.ownKeys(l).filter((h) => {
          var c = n.get(h);
          return c === void 0 || c.v !== z;
        });
        for (var [f, p] of n)
          p.v !== z && !(f in l) && o.push(f);
        return o;
      },
      setPrototypeOf() {
        Ti();
      }
    }
  );
}
var Jn, kr, Tr, Sr;
function kn() {
  if (Jn === void 0) {
    Jn = window, kr = /Firefox/.test(navigator.userAgent);
    var e = Element.prototype, t = Node.prototype, n = Text.prototype;
    Tr = gt(t, "firstChild").get, Sr = gt(t, "nextSibling").get, Xn(e) && (e.__click = void 0, e.__className = void 0, e.__attributes = null, e.__style = void 0, e.__e = void 0), Xn(n) && (n.__t = void 0);
  }
}
function qe(e = "") {
  return document.createTextNode(e);
}
// @__NO_SIDE_EFFECTS__
function He(e) {
  return Tr.call(e);
}
// @__NO_SIDE_EFFECTS__
function Oe(e) {
  return Sr.call(e);
}
function Me(e, t) {
  if (!$)
    return /* @__PURE__ */ He(e);
  var n = (
    /** @type {TemplateNode} */
    /* @__PURE__ */ He(x)
  );
  if (n === null)
    n = x.appendChild(qe());
  else if (t && n.nodeType !== Ln) {
    var i = qe();
    return n == null || n.before(i), L(i), i;
  }
  return L(n), n;
}
function Ui(e, t = !1) {
  if (!$) {
    var n = (
      /** @type {DocumentFragment} */
      /* @__PURE__ */ He(
        /** @type {Node} */
        e
      )
    );
    return n instanceof Comment && n.data === "" ? /* @__PURE__ */ Oe(n) : n;
  }
  if (t && (x == null ? void 0 : x.nodeType) !== Ln) {
    var i = qe();
    return x == null || x.before(i), L(i), i;
  }
  return x;
}
function Gt(e, t = 1, n = !1) {
  let i = $ ? x : e;
  for (var r; t--; )
    r = i, i = /** @type {TemplateNode} */
    /* @__PURE__ */ Oe(i);
  if (!$)
    return i;
  if (n && (i == null ? void 0 : i.nodeType) !== Ln) {
    var s = qe();
    return i === null ? r == null || r.after(s) : i.before(s), L(s), s;
  }
  return L(i), /** @type {TemplateNode} */
  i;
}
function Cr(e) {
  e.textContent = "";
}
function qr() {
  return !1;
}
function Or(e) {
  var t = E, n = k;
  Y(null), _e(null);
  try {
    return e();
  } finally {
    Y(t), _e(n);
  }
}
function Wi(e) {
  k === null && E === null && bi(), E !== null && (E.f & he) !== 0 && k === null && $i(), dt && wi();
}
function Xi(e, t) {
  var n = t.last;
  n === null ? t.last = t.first = e : (n.next = e, e.prev = n, t.last = e);
}
function Ae(e, t, n, i = !0) {
  var r = k;
  r !== null && (r.f & $e) !== 0 && (e |= $e);
  var s = {
    ctx: fe,
    deps: null,
    nodes_start: null,
    nodes_end: null,
    f: e | oe,
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
      rn(s), s.f |= zn;
    } catch (o) {
      throw ne(s), o;
    }
  else t !== null && lt(s);
  if (i) {
    var a = s;
    if (n && a.deps === null && a.teardown === null && a.nodes_start === null && a.first === a.last && // either `null`, or a singular child
    (a.f & ct) === 0 && (a = a.first), a !== null && (a.parent = r, r !== null && Xi(a, r), E !== null && (E.f & J) !== 0 && (e & Ue) === 0)) {
      var l = (
        /** @type {Derived} */
        E
      );
      (l.effects ?? (l.effects = [])).push(a);
    }
  }
  return s;
}
function Gi() {
  return E !== null && !we;
}
function Ki(e) {
  const t = Ae(Pn, null, !1);
  return K(t, W), t.teardown = e, t;
}
function Kt(e) {
  Wi();
  var t = (
    /** @type {Effect} */
    k.f
  ), n = !E && (t & Pe) !== 0 && (t & zn) === 0;
  if (n) {
    var i = (
      /** @type {ComponentContext} */
      fe
    );
    (i.e ?? (i.e = [])).push(e);
  } else
    return Ar(e);
}
function Ar(e) {
  return Ae(In | hi, e, !1);
}
function Ji(e) {
  Ce.ensure();
  const t = Ae(Ue | ct, e, !0);
  return () => {
    ne(t);
  };
}
function Zi(e) {
  Ce.ensure();
  const t = Ae(Ue | ct, e, !0);
  return (n = {}) => new Promise((i) => {
    n.outro ? it(t, () => {
      ne(t), i(void 0);
    }) : (ne(t), i(void 0));
  });
}
function Nr(e) {
  return Ae(In, e, !1);
}
function Qi(e) {
  return Ae(Dn | ct, e, !0);
}
function Vn(e, t = 0) {
  return Ae(Pn | t, e, !0);
}
function ze(e, t = [], n = []) {
  Fi(t, n, (i) => {
    Ae(Pn, () => e(...i.map(g)), !0);
  });
}
function dn(e, t = 0) {
  var n = Ae(ft | t, e, !0);
  return n;
}
function le(e, t = !0) {
  return Ae(Pe | ct, e, !0, t);
}
function Rr(e) {
  var t = e.teardown;
  if (t !== null) {
    const n = dt, i = E;
    Qn(!0), Y(null);
    try {
      t.call(null);
    } finally {
      Qn(n), Y(i);
    }
  }
}
function jr(e, t = !1) {
  var n = e.first;
  for (e.first = e.last = null; n !== null; ) {
    const r = n.ac;
    r !== null && Or(() => {
      r.abort(_t);
    });
    var i = n.next;
    (n.f & Ue) !== 0 ? n.parent = null : ne(n, t), n = i;
  }
}
function es(e) {
  for (var t = e.first; t !== null; ) {
    var n = t.next;
    (t.f & Pe) === 0 && ne(t), t = n;
  }
}
function ne(e, t = !0) {
  var n = !1;
  (t || (e.f & vi) !== 0) && e.nodes_start !== null && e.nodes_end !== null && (ts(
    e.nodes_start,
    /** @type {TemplateNode} */
    e.nodes_end
  ), n = !0), jr(e, t && !n), nn(e, 0), K(e, ut);
  var i = e.transitions;
  if (i !== null)
    for (const s of i)
      s.stop();
  Rr(e);
  var r = e.parent;
  r !== null && r.first !== null && Ir(e), e.next = e.prev = e.teardown = e.ctx = e.deps = e.fn = e.nodes_start = e.nodes_end = e.ac = null;
}
function ts(e, t) {
  for (; e !== null; ) {
    var n = e === t ? null : (
      /** @type {TemplateNode} */
      /* @__PURE__ */ Oe(e)
    );
    e.remove(), e = n;
  }
}
function Ir(e) {
  var t = e.parent, n = e.prev, i = e.next;
  n !== null && (n.next = i), i !== null && (i.prev = n), t !== null && (t.first === e && (t.first = i), t.last === e && (t.last = n));
}
function it(e, t) {
  var n = [];
  Hn(e, n, !0), Pr(n, () => {
    ne(e), t && t();
  });
}
function Pr(e, t) {
  var n = e.length;
  if (n > 0) {
    var i = () => --n || t();
    for (var r of e)
      r.out(i);
  } else
    t();
}
function Hn(e, t, n) {
  if ((e.f & $e) === 0) {
    if (e.f ^= $e, e.transitions !== null)
      for (const a of e.transitions)
        (a.is_global || n) && t.push(a);
    for (var i = e.first; i !== null; ) {
      var r = i.next, s = (i.f & Dt) !== 0 || (i.f & Pe) !== 0;
      Hn(i, t, s ? n : !1), i = r;
    }
  }
}
function vn(e) {
  Mr(e, !0);
}
function Mr(e, t) {
  if ((e.f & $e) !== 0) {
    e.f ^= $e, (e.f & W) === 0 && (K(e, oe), lt(e));
    for (var n = e.first; n !== null; ) {
      var i = n.next, r = (n.f & Dt) !== 0 || (n.f & Pe) !== 0;
      Mr(n, r ? t : !1), n = i;
    }
    if (e.transitions !== null)
      for (const s of e.transitions)
        (s.is_global || t) && s.in();
  }
}
let mt = !1;
function Zn(e) {
  mt = e;
}
let dt = !1;
function Qn(e) {
  dt = e;
}
let E = null, we = !1;
function Y(e) {
  E = e;
}
let k = null;
function _e(e) {
  k = e;
}
let G = null;
function zr(e) {
  E !== null && (G === null ? G = [e] : G.push(e));
}
let U = null, ie = 0, ue = null;
function ns(e) {
  ue = e;
}
let Dr = 1, jt = 0, st = jt;
function er(e) {
  st = e;
}
let Ye = !1;
function Lr() {
  return ++Dr;
}
function hn(e) {
  var h;
  var t = e.f;
  if ((t & oe) !== 0)
    return !0;
  if ((t & We) !== 0) {
    var n = e.deps, i = (t & he) !== 0;
    if (n !== null) {
      var r, s, a = (t & Qt) !== 0, l = i && k !== null && !Ye, o = n.length;
      if ((a || l) && (k === null || (k.f & ut) === 0)) {
        var f = (
          /** @type {Derived} */
          e
        ), p = f.parent;
        for (r = 0; r < o; r++)
          s = n[r], (a || !((h = s == null ? void 0 : s.reactions) != null && h.includes(f))) && (s.reactions ?? (s.reactions = [])).push(f);
        a && (f.f ^= Qt), l && p !== null && (p.f & he) === 0 && (f.f ^= he);
      }
      for (r = 0; r < o; r++)
        if (s = n[r], hn(
          /** @type {Derived} */
          s
        ) && br(
          /** @type {Derived} */
          s
        ), s.wv > e.wv)
          return !0;
    }
    (!i || k !== null && !Ye) && K(e, W);
  }
  return !1;
}
function Fr(e, t, n = !0) {
  var i = e.reactions;
  if (i !== null && !(G != null && G.includes(e)))
    for (var r = 0; r < i.length; r++) {
      var s = i[r];
      (s.f & J) !== 0 ? Fr(
        /** @type {Derived} */
        s,
        t,
        !1
      ) : t === s && (n ? K(s, oe) : (s.f & W) !== 0 && K(s, We), lt(
        /** @type {Effect} */
        s
      ));
    }
}
function Br(e) {
  var m;
  var t = U, n = ie, i = ue, r = E, s = Ye, a = G, l = fe, o = we, f = st, p = e.f;
  U = /** @type {null | Value[]} */
  null, ie = 0, ue = null, Ye = (p & he) !== 0 && (we || !mt || E === null), E = (p & (Pe | Ue)) === 0 ? e : null, G = null, Tt(e.ctx), we = !1, st = ++jt, e.ac !== null && (Or(() => {
    e.ac.abort(_t);
  }), e.ac = null);
  try {
    e.f |= mn;
    var h = (
      /** @type {Function} */
      e.fn
    ), c = h(), d = e.deps;
    if (U !== null) {
      var v;
      if (nn(e, ie), d !== null && ie > 0)
        for (d.length = ie + U.length, v = 0; v < U.length; v++)
          d[ie + v] = U[v];
      else
        e.deps = d = U;
      if (!Ye || // Deriveds that already have reactions can cleanup, so we still add them as reactions
      (p & J) !== 0 && /** @type {import('#client').Derived} */
      e.reactions !== null)
        for (v = ie; v < d.length; v++)
          ((m = d[v]).reactions ?? (m.reactions = [])).push(e);
    } else d !== null && ie < d.length && (nn(e, ie), d.length = ie);
    if (dr() && ue !== null && !we && d !== null && (e.f & (J | We | oe)) === 0)
      for (v = 0; v < /** @type {Source[]} */
      ue.length; v++)
        Fr(
          ue[v],
          /** @type {Effect} */
          e
        );
    return r !== null && r !== e && (jt++, ue !== null && (i === null ? i = ue : i.push(.../** @type {Source[]} */
    ue))), (e.f & rt) !== 0 && (e.f ^= rt), c;
  } catch (y) {
    return hr(y);
  } finally {
    e.f ^= mn, U = t, ie = n, ue = i, E = r, Ye = s, G = a, Tt(l), we = o, st = f;
  }
}
function rs(e, t) {
  let n = t.reactions;
  if (n !== null) {
    var i = oi.call(n, e);
    if (i !== -1) {
      var r = n.length - 1;
      r === 0 ? n = t.reactions = null : (n[i] = n[r], n.pop());
    }
  }
  n === null && (t.f & J) !== 0 && // Destroying a child effect while updating a parent effect can cause a dependency to appear
  // to be unused, when in fact it is used by the currently-updating parent. Checking `new_deps`
  // allows us to skip the expensive work of disconnecting and immediately reconnecting it
  (U === null || !U.includes(t)) && (K(t, We), (t.f & (he | Qt)) === 0 && (t.f ^= Qt), $r(
    /** @type {Derived} **/
    t
  ), nn(
    /** @type {Derived} **/
    t,
    0
  ));
}
function nn(e, t) {
  var n = e.deps;
  if (n !== null)
    for (var i = t; i < n.length; i++)
      rs(e, n[i]);
}
function rn(e) {
  var t = e.f;
  if ((t & ut) === 0) {
    K(e, W);
    var n = k, i = mt;
    k = e, mt = !0;
    try {
      (t & ft) !== 0 ? es(e) : jr(e), Rr(e);
      var r = Br(e);
      e.teardown = typeof r == "function" ? r : null, e.wv = Dr;
      var s;
      ar && Ni && (e.f & oe) !== 0 && e.deps;
    } finally {
      mt = i, k = n;
    }
  }
}
function g(e) {
  var t = e.f, n = (t & J) !== 0;
  if (E !== null && !we) {
    var i = k !== null && (k.f & ut) !== 0;
    if (!i && !(G != null && G.includes(e))) {
      var r = E.deps;
      if ((E.f & mn) !== 0)
        e.rv < jt && (e.rv = jt, U === null && r !== null && r[ie] === e ? ie++ : U === null ? U = [e] : (!Ye || !U.includes(e)) && U.push(e));
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
    l !== null && (l.f & he) === 0 && (a.f ^= he);
  }
  if (dt) {
    if (Ve.has(e))
      return Ve.get(e);
    if (n) {
      a = /** @type {Derived} */
      e;
      var o = a.v;
      return ((a.f & W) === 0 && a.reactions !== null || Yr(a)) && (o = Yn(a)), Ve.set(a, o), o;
    }
  } else if (n) {
    if (a = /** @type {Derived} */
    e, D != null && D.has(a))
      return D.get(a);
    hn(a) && br(a);
  }
  if (D != null && D.has(e))
    return D.get(e);
  if ((e.f & rt) !== 0)
    throw e.v;
  return e.v;
}
function Yr(e) {
  if (e.v === z) return !0;
  if (e.deps === null) return !1;
  for (const t of e.deps)
    if (Ve.has(t) || (t.f & J) !== 0 && Yr(
      /** @type {Derived} */
      t
    ))
      return !0;
  return !1;
}
function Un(e) {
  var t = we;
  try {
    return we = !0, e();
  } finally {
    we = t;
  }
}
const is = -7169;
function K(e, t) {
  e.f = e.f & is | t;
}
const Vr = /* @__PURE__ */ new Set(), Tn = /* @__PURE__ */ new Set();
function ss(e) {
  for (var t = 0; t < e.length; t++)
    Vr.add(e[t]);
  for (var n of Tn)
    n(e);
}
let tr = null;
function Vt(e) {
  var C;
  var t = this, n = (
    /** @type {Node} */
    t.ownerDocument
  ), i = e.type, r = ((C = e.composedPath) == null ? void 0 : C.call(e)) || [], s = (
    /** @type {null | Element} */
    r[0] || e.target
  );
  tr = e;
  var a = 0, l = tr === e && e.__root;
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
    xt(e, "currentTarget", {
      configurable: !0,
      get() {
        return s || n;
      }
    });
    var p = E, h = k;
    Y(null), _e(null);
    try {
      for (var c, d = []; s !== null; ) {
        var v = s.assignedSlot || s.parentNode || /** @type {any} */
        s.host || null;
        try {
          var m = s["__" + i];
          if (m != null && (!/** @type {any} */
          s.disabled || // DOM could've been updated already by the time this is reached, so we check this as well
          // -> the target could not have been disabled because it emits the event in the first place
          e.target === s))
            if (Rn(m)) {
              var [y, ...N] = m;
              y.apply(s, [e, ...N]);
            } else
              m.call(s, e);
        } catch (T) {
          c ? d.push(T) : c = T;
        }
        if (e.cancelBubble || v === t || v === null)
          break;
        s = v;
      }
      if (c) {
        for (let T of d)
          queueMicrotask(() => {
            throw T;
          });
        throw c;
      }
    } finally {
      e.__root = t, delete e.currentTarget, Y(p), _e(h);
    }
  }
}
function as(e) {
  var t = document.createElement("template");
  return t.innerHTML = e.replaceAll("<!>", "<!---->"), t.content;
}
function at(e, t) {
  var n = (
    /** @type {Effect} */
    k
  );
  n.nodes_start === null && (n.nodes_start = e, n.nodes_end = t);
}
// @__NO_SIDE_EFFECTS__
function vt(e, t) {
  var n = (t & ii) !== 0, i = (t & si) !== 0, r, s = !e.startsWith("<!>");
  return () => {
    if ($)
      return at(x, null), x;
    r === void 0 && (r = as(s ? e : "<!>" + e), n || (r = /** @type {Node} */
    /* @__PURE__ */ He(r)));
    var a = (
      /** @type {TemplateNode} */
      i || kr ? document.importNode(r, !0) : r.cloneNode(!0)
    );
    if (n) {
      var l = (
        /** @type {TemplateNode} */
        /* @__PURE__ */ He(a)
      ), o = (
        /** @type {TemplateNode} */
        a.lastChild
      );
      at(l, o);
    } else
      at(a, a);
    return a;
  };
}
function ls() {
  if ($)
    return at(x, null), x;
  var e = document.createDocumentFragment(), t = document.createComment(""), n = qe();
  return e.append(t, n), at(t, n), e;
}
function je(e, t) {
  if ($) {
    k.nodes_end = x, kt();
    return;
  }
  e !== null && e.before(
    /** @type {Node} */
    t
  );
}
const os = ["touchstart", "touchmove"];
function fs(e) {
  return os.includes(e);
}
const us = (
  /** @type {const} */
  ["textarea", "script", "style", "title"]
);
function cs(e) {
  return us.includes(
    /** @type {typeof RAW_TEXT_ELEMENTS[number]} */
    e
  );
}
function ds(e, t) {
  var n = t == null ? "" : typeof t == "object" ? t + "" : t;
  n !== (e.__t ?? (e.__t = e.nodeValue)) && (e.__t = n, e.nodeValue = n + "");
}
function Hr(e, t) {
  return Ur(e, t);
}
function vs(e, t) {
  kn(), t.intro = t.intro ?? !1;
  const n = t.target, i = $, r = x;
  try {
    for (var s = (
      /** @type {TemplateNode} */
      /* @__PURE__ */ He(n)
    ); s && (s.nodeType !== Ct || /** @type {Comment} */
    s.data !== sr); )
      s = /** @type {TemplateNode} */
      /* @__PURE__ */ Oe(s);
    if (!s)
      throw Et;
    X(!0), L(
      /** @type {Comment} */
      s
    );
    const a = Ur(e, { ...t, anchor: s });
    return X(!1), /**  @type {Exports} */
    a;
  } catch (a) {
    if (a instanceof Error && a.message.split(`
`).some((l) => l.startsWith("https://svelte.dev/e/")))
      throw a;
    return a !== Et && console.warn("Failed to hydrate: ", a), t.recover === !1 && xi(), kn(), Cr(n), X(!1), Hr(e, t);
  } finally {
    X(i), L(r);
  }
}
const pt = /* @__PURE__ */ new Map();
function Ur(e, { target: t, anchor: n, props: i = {}, events: r, context: s, intro: a = !0 }) {
  kn();
  var l = /* @__PURE__ */ new Set(), o = (h) => {
    for (var c = 0; c < h.length; c++) {
      var d = h[c];
      if (!l.has(d)) {
        l.add(d);
        var v = fs(d);
        t.addEventListener(d, Vt, { passive: v });
        var m = pt.get(d);
        m === void 0 ? (document.addEventListener(d, Vt, { passive: v }), pt.set(d, 1)) : pt.set(d, m + 1);
      }
    }
  };
  o(jn(Vr)), Tn.add(o);
  var f = void 0, p = Zi(() => {
    var h = n ?? t.appendChild(qe());
    return zi(
      /** @type {TemplateNode} */
      h,
      {
        pending: () => {
        }
      },
      (c) => {
        if (s) {
          Fn({});
          var d = (
            /** @type {ComponentContext} */
            fe
          );
          d.c = s;
        }
        if (r && (i.$$events = r), $ && at(
          /** @type {TemplateNode} */
          c,
          null
        ), f = e(c, i) || {}, $ && (k.nodes_end = x, x === null || x.nodeType !== Ct || /** @type {Comment} */
        x.data !== Nn))
          throw fn(), Et;
        s && Bn();
      }
    ), () => {
      var v;
      for (var c of l) {
        t.removeEventListener(c, Vt);
        var d = (
          /** @type {number} */
          pt.get(c)
        );
        --d === 0 ? (document.removeEventListener(c, Vt), pt.delete(c)) : pt.set(c, d);
      }
      Tn.delete(o), h !== n && ((v = h.parentNode) == null || v.removeChild(h));
    };
  });
  return Sn.set(f, p), f;
}
let Sn = /* @__PURE__ */ new WeakMap();
function hs(e, t) {
  const n = Sn.get(e);
  return n ? (Sn.delete(e), n(t)) : Promise.resolve();
}
function Wr(e) {
  fe === null && mi(), Kt(() => {
    const t = Un(e);
    if (typeof t == "function") return (
      /** @type {() => void} */
      t
    );
  });
}
function Ot(e, t, n = !1) {
  $ && kt();
  var i = e, r = null, s = null, a = z, l = n ? Dt : 0, o = !1;
  const f = (d, v = !0) => {
    o = !0, c(v, d);
  };
  var p = null;
  function h() {
    p !== null && (p.lastChild.remove(), i.before(p), p = null);
    var d = a ? r : s, v = a ? s : r;
    d && vn(d), v && it(v, () => {
      a ? s = null : r = null;
    });
  }
  const c = (d, v) => {
    if (a === (a = d)) return;
    let m = !1;
    if ($) {
      const q = fr(i) === on;
      !!a === q && (i = en(), L(i), X(!1), m = !0);
    }
    var y = qr(), N = i;
    if (y && (p = document.createDocumentFragment(), p.append(N = qe())), a ? r ?? (r = v && le(() => v(N))) : s ?? (s = v && le(() => v(N))), y) {
      var C = (
        /** @type {Batch} */
        j
      ), T = a ? r : s, _ = a ? s : r;
      T && C.skipped_effects.delete(T), _ && C.skipped_effects.add(_), C.add_callback(h);
    } else
      h();
    m && X(!0);
  };
  dn(() => {
    o = !1, t(f), o || c(null, null);
  }, l), $ && (i = x);
}
function ps(e, t, n) {
  for (var i = e.items, r = [], s = t.length, a = 0; a < s; a++)
    Hn(t[a].e, r, !0);
  var l = s > 0 && r.length === 0 && n !== null;
  if (l) {
    var o = (
      /** @type {Element} */
      /** @type {Element} */
      n.parentNode
    );
    Cr(o), o.append(
      /** @type {Element} */
      n
    ), i.clear(), Ee(e, t[0].prev, t[s - 1].next);
  }
  Pr(r, () => {
    for (var f = 0; f < s; f++) {
      var p = t[f];
      l || (i.delete(p.k), Ee(e, p.prev, p.next)), ne(p.e, !l);
    }
  });
}
function _s(e, t, n, i, r, s = null) {
  var a = e, l = { flags: t, items: /* @__PURE__ */ new Map(), first: null };
  {
    var o = (
      /** @type {Element} */
      e
    );
    a = $ ? L(
      /** @type {Comment | Text} */
      /* @__PURE__ */ He(o)
    ) : o.appendChild(qe());
  }
  $ && kt();
  var f = null, p = !1, h = /* @__PURE__ */ new Map(), c = /* @__PURE__ */ Vi(() => {
    var y = n();
    return Rn(y) ? y : y == null ? [] : jn(y);
  }), d, v;
  function m() {
    gs(
      v,
      d,
      l,
      h,
      a,
      r,
      t,
      i,
      n
    ), s !== null && (d.length === 0 ? f ? vn(f) : f = le(() => s(a)) : f !== null && it(f, () => {
      f = null;
    }));
  }
  dn(() => {
    v ?? (v = /** @type {Effect} */
    k), d = /** @type {V[]} */
    g(c);
    var y = d.length;
    if (p && y === 0)
      return;
    p = y === 0;
    let N = !1;
    if ($) {
      var C = fr(a) === on;
      C !== (y === 0) && (a = en(), L(a), X(!1), N = !0);
    }
    if ($) {
      for (var T = null, _, q = 0; q < y; q++) {
        if (x.nodeType === Ct && /** @type {Comment} */
        x.data === Nn) {
          a = /** @type {Comment} */
          x, N = !0, X(!1);
          break;
        }
        var Z = d[q], I = i(Z, q);
        _ = Cn(
          x,
          l,
          T,
          null,
          Z,
          I,
          q,
          r,
          t,
          n
        ), l.items.set(I, _), T = _;
      }
      y > 0 && L(en());
    }
    if ($)
      y === 0 && s && (f = le(() => s(a)));
    else if (qr()) {
      var V = /* @__PURE__ */ new Set(), Q = (
        /** @type {Batch} */
        j
      );
      for (q = 0; q < y; q += 1) {
        Z = d[q], I = i(Z, q);
        var ht = l.items.get(I) ?? h.get(I);
        ht || (_ = Cn(
          null,
          l,
          null,
          null,
          Z,
          I,
          q,
          r,
          t,
          n,
          !0
        ), h.set(I, _)), V.add(I);
      }
      for (const [Xe, Ge] of l.items)
        V.has(Xe) || Q.skipped_effects.add(Ge.e);
      Q.add_callback(m);
    } else
      m();
    N && X(!0), g(c);
  }), $ && (a = x);
}
function gs(e, t, n, i, r, s, a, l, o) {
  var f = t.length, p = n.items, h = n.first, c = h, d, v = null, m = [], y = [], N, C, T, _;
  for (_ = 0; _ < f; _ += 1) {
    if (N = t[_], C = l(N, _), T = p.get(C), T === void 0) {
      var q = i.get(C);
      if (q !== void 0) {
        i.delete(C), p.set(C, q);
        var Z = v ? v.next : c;
        Ee(n, v, q), Ee(n, q, Z), gn(q, Z, r), v = q;
      } else {
        var I = c ? (
          /** @type {TemplateNode} */
          c.e.nodes_start
        ) : r;
        v = Cn(
          I,
          n,
          v,
          v === null ? n.first : v.next,
          N,
          C,
          _,
          s,
          a,
          o
        );
      }
      p.set(C, v), m = [], y = [], c = v.next;
      continue;
    }
    if ((T.e.f & $e) !== 0 && vn(T.e), T !== c) {
      if (d !== void 0 && d.has(T)) {
        if (m.length < y.length) {
          var V = y[0], Q;
          v = V.prev;
          var ht = m[0], Xe = m[m.length - 1];
          for (Q = 0; Q < m.length; Q += 1)
            gn(m[Q], V, r);
          for (Q = 0; Q < y.length; Q += 1)
            d.delete(y[Q]);
          Ee(n, ht.prev, Xe.next), Ee(n, v, ht), Ee(n, Xe, V), c = V, v = Xe, _ -= 1, m = [], y = [];
        } else
          d.delete(T), gn(T, c, r), Ee(n, T.prev, T.next), Ee(n, T, v === null ? n.first : v.next), Ee(n, v, T), v = T;
        continue;
      }
      for (m = [], y = []; c !== null && c.k !== C; )
        (c.e.f & $e) === 0 && (d ?? (d = /* @__PURE__ */ new Set())).add(c), y.push(c), c = c.next;
      if (c === null)
        continue;
      T = c;
    }
    m.push(T), v = T, c = T.next;
  }
  if (c !== null || d !== void 0) {
    for (var Ge = d === void 0 ? [] : jn(d); c !== null; )
      (c.e.f & $e) === 0 && Ge.push(c), c = c.next;
    var pn = Ge.length;
    if (pn > 0) {
      var Lt = f === 0 ? r : null;
      ps(n, Ge, Lt);
    }
  }
  e.first = n.first && n.first.e, e.last = v && v.e;
  for (var Ft of i.values())
    ne(Ft.e);
  i.clear();
}
function Cn(e, t, n, i, r, s, a, l, o, f, p) {
  var h = (o & ti) !== 0, c = (o & ri) === 0, d = h ? c ? /* @__PURE__ */ Er(r, !1, !1) : ot(r) : r, v = (o & ni) === 0 ? a : ot(a), m = {
    i: v,
    v: d,
    k: s,
    a: null,
    // @ts-expect-error
    e: null,
    prev: n,
    next: i
  };
  try {
    if (e === null) {
      var y = document.createDocumentFragment();
      y.append(e = qe());
    }
    return m.e = le(() => l(
      /** @type {Node} */
      e,
      d,
      v,
      f
    ), $), m.e.prev = n && n.e, m.e.next = i && i.e, n === null ? p || (t.first = m) : (n.next = m, n.e.next = m.e), i !== null && (i.prev = m, i.e.prev = m.e), m;
  } finally {
  }
}
function gn(e, t, n) {
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
      /* @__PURE__ */ Oe(s)
    );
    r.before(s), s = a;
  }
}
function Ee(e, t, n) {
  t === null ? e.first = n : (t.next = n, t.e.next = n && n.e), n !== null && (n.prev = t, n.e.prev = t && t.e);
}
function ms(e, t, n, i, r, s) {
  let a = $;
  $ && kt();
  var l, o, f = null;
  $ && x.nodeType === gi && (f = /** @type {Element} */
  x, kt());
  var p = (
    /** @type {TemplateNode} */
    $ ? x : e
  ), h;
  dn(() => {
    const c = t() || null;
    var d = c === "svg" ? li : null;
    c !== l && (h && (c === null ? it(h, () => {
      h = null, o = null;
    }) : c === o ? vn(h) : ne(h)), c && c !== o && (h = le(() => {
      if (f = $ ? (
        /** @type {Element} */
        f
      ) : d ? document.createElementNS(d, c) : document.createElement(c), at(f, f), i) {
        $ && cs(c) && f.append(document.createComment(""));
        var v = (
          /** @type {TemplateNode} */
          $ ? /* @__PURE__ */ He(f) : f.appendChild(qe())
        );
        $ && (v === null ? X(!1) : L(v)), i(f, v);
      }
      k.nodes_end = f, p.before(f);
    })), l = c, l && (o = l));
  }, Dt), a && (X(!0), L(p));
}
function Xr(e, t) {
  Nr(() => {
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
function ys(e, t, n) {
  var i = e == null ? "" : "" + e;
  return t && (i = i ? i + " " + t : t), i === "" ? null : i;
}
function ws(e, t) {
  return e == null ? null : String(e);
}
function me(e, t, n, i, r, s) {
  var a = e.__className;
  if ($ || a !== n || a === void 0) {
    var l = ys(n, i);
    (!$ || l !== e.getAttribute("class")) && (l == null ? e.removeAttribute("class") : t ? e.className = l : e.setAttribute("class", l)), e.__className = n;
  }
  return s;
}
function De(e, t, n, i) {
  var r = e.__style;
  if ($ || r !== t) {
    var s = ws(t);
    (!$ || s !== e.getAttribute("style")) && (s == null ? e.removeAttribute("style") : e.style.cssText = s), e.__style = t;
  }
  return i;
}
const $s = Symbol("is custom element"), bs = Symbol("is html");
function Gr(e, t, n, i) {
  var r = Es(e);
  $ && (r[t] = e.getAttribute(t), t === "src" || t === "srcset" || t === "href" && e.nodeName === "LINK") || r[t] !== (r[t] = n) && (t === "loading" && (e[_i] = n), n == null ? e.removeAttribute(t) : typeof n != "string" && Kr(e).includes(t) ? e[t] = n : e.setAttribute(t, n));
}
function nr(e, t, n) {
  var i = E, r = k;
  let s = $;
  $ && X(!1), Y(null), _e(null);
  try {
    // `style` should use `set_attribute` rather than the setter
    t !== "style" && // Don't compute setters for custom elements while they aren't registered yet,
    // because during their upgrade/instantiation they might add more setters.
    // Instead, fall back to a simple "an object, then set as property" heuristic.
    (qn.has(e.getAttribute("is") || e.nodeName) || // customElements may not be available in browser extension contexts
    !customElements || customElements.get(e.getAttribute("is") || e.tagName.toLowerCase()) ? Kr(e).includes(t) : n && typeof n == "object") ? e[t] = n : Gr(e, t, n == null ? n : String(n));
  } finally {
    Y(i), _e(r), s && X(!0);
  }
}
function Es(e) {
  return (
    /** @type {Record<string | symbol, unknown>} **/
    // @ts-expect-error
    e.__attributes ?? (e.__attributes = {
      [$s]: e.nodeName.includes("-"),
      [bs]: e.namespaceURI === ai
    })
  );
}
var qn = /* @__PURE__ */ new Map();
function Kr(e) {
  var t = e.getAttribute("is") || e.nodeName, n = qn.get(t);
  if (n) return n;
  qn.set(t, n = []);
  for (var i, r = e, s = Element.prototype; s !== r; ) {
    i = fi(r);
    for (var a in i)
      i[a].set && n.push(a);
    r = lr(r);
  }
  return n;
}
function rr(e, t) {
  return e === t || (e == null ? void 0 : e[Ht]) === t;
}
function xs(e = {}, t, n, i) {
  return Nr(() => {
    var r, s;
    return Vn(() => {
      r = s, s = [], Un(() => {
        e !== n(...s) && (t(e, ...s), r && rr(n(...r), e) && t(null, ...r));
      });
    }), () => {
      Rt(() => {
        s && rr(n(...s), e) && t(null, ...s);
      });
    };
  }), e;
}
function ce(e, t, n, i) {
  var r = (
    /** @type {V} */
    i
  ), s = !0, a = () => (s && (s = !1, r = /** @type {V} */
  i), r), l;
  l = /** @type {V} */
  e[t], l === void 0 && i !== void 0 && (l = a());
  var o;
  o = () => {
    var c = (
      /** @type {V} */
      e[t]
    );
    return c === void 0 ? a() : (s = !0, c);
  };
  var f = !1, p = /* @__PURE__ */ cn(() => (f = !1, o())), h = (
    /** @type {Effect} */
    k
  );
  return (
    /** @type {() => V} */
    (function(c, d) {
      if (arguments.length > 0) {
        const v = d ? g(p) : c;
        return O(p, v), f = !0, r !== void 0 && (r = v), c;
      }
      return dt && f || (h.f & ut) !== 0 ? p.v : g(p);
    })
  );
}
function ks(e) {
  return new Ts(e);
}
var Ie, ve;
class Ts {
  /**
   * @param {ComponentConstructorOptions & {
   *  component: any;
   * }} options
   */
  constructor(t) {
    /** @type {any} */
    S(this, Ie);
    /** @type {Record<string, any>} */
    S(this, ve);
    var s;
    var n = /* @__PURE__ */ new Map(), i = (a, l) => {
      var o = /* @__PURE__ */ Er(l, !1, !1);
      return n.set(a, o), o;
    };
    const r = new Proxy(
      { ...t.props || {}, $$events: {} },
      {
        get(a, l) {
          return g(n.get(l) ?? i(l, Reflect.get(a, l)));
        },
        has(a, l) {
          return l === pi ? !0 : (g(n.get(l) ?? i(l, Reflect.get(a, l))), Reflect.has(a, l));
        },
        set(a, l, o) {
          return O(n.get(l) ?? i(l, o), o), Reflect.set(a, l, o);
        }
      }
    );
    w(this, ve, (t.hydrate ? vs : Hr)(t.component, {
      target: t.target,
      anchor: t.anchor,
      props: r,
      context: t.context,
      intro: t.intro ?? !1,
      recover: t.recover
    })), (!((s = t == null ? void 0 : t.props) != null && s.$$host) || t.sync === !1) && ae(), w(this, Ie, r.$$events);
    for (const a of Object.keys(u(this, ve)))
      a === "$set" || a === "$destroy" || a === "$on" || xt(this, a, {
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
      hs(u(this, ve));
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
    u(this, Ie)[t] = u(this, Ie)[t] || [];
    const i = (...r) => n.call(this, ...r);
    return u(this, Ie)[t].push(i), () => {
      u(this, Ie)[t] = u(this, Ie)[t].filter(
        /** @param {any} fn */
        (r) => r !== i
      );
    };
  }
  $destroy() {
    u(this, ve).$destroy();
  }
}
Ie = new WeakMap(), ve = new WeakMap();
let Jr;
typeof HTMLElement == "function" && (Jr = class extends HTMLElement {
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
          r !== "default" && (a.name = r), je(s, a);
        };
      };
      if (await Promise.resolve(), !this.$$cn || this.$$c)
        return;
      const n = {}, i = Ss(this);
      for (const r of this.$$s)
        r in i && (r === "default" && !this.$$d.children ? (this.$$d.children = t(r), n.default = !0) : n[r] = t(r));
      for (const r of this.attributes) {
        const s = this.$$g_p(r.name);
        s in this.$$d || (this.$$d[s] = Jt(s, r.value, this.$$p_d, "toProp"));
      }
      for (const r in this.$$p_d)
        !(r in this.$$d) && this[r] !== void 0 && (this.$$d[r] = this[r], delete this[r]);
      this.$$c = ks({
        component: this.$$ctor,
        target: this.shadowRoot || this,
        props: {
          ...this.$$d,
          $$slots: n,
          $$host: this
        }
      }), this.$$me = Ji(() => {
        Vn(() => {
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
function Ss(e) {
  const t = {};
  return e.childNodes.forEach((n) => {
    t[
      /** @type {Element} node */
      n.slot || "default"
    ] = !0;
  }), t;
}
function Zr(e, t, n, i, r, s) {
  let a = class extends Jr {
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
    xt(a.prototype, l, {
      get() {
        return this.$$c && l in this.$$c ? this.$$c[l] : this.$$d[l];
      },
      set(o) {
        var h;
        o = Jt(l, o, t), this.$$d[l] = o;
        var f = this.$$c;
        if (f) {
          var p = (h = gt(f, l)) == null ? void 0 : h.get;
          p ? f[l] = o : f.$set({ [l]: o });
        }
      }
    });
  }), i.forEach((l) => {
    xt(a.prototype, l, {
      get() {
        var o;
        return (o = this.$$c) == null ? void 0 : o[l];
      }
    });
  }), s && (a = s(a)), e.element = /** @type {any} */
  a, a;
}
var Cs = /* @__PURE__ */ vt('<span class="loading svelte-lv9s7p">Loading...</span>'), qs = /* @__PURE__ */ vt("<div><!> <!></div>");
const Os = {
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
function On(e, t) {
  Fn(t, !0), Xr(e, Os);
  const n = ce(t, "type", 7, "div"), i = ce(t, "config"), r = ce(t, "hass"), s = ce(t, "preview"), a = ce(t, "marginTop", 7, "0px"), l = ce(t, "open"), o = ce(t, "animation", 7, !0), f = ce(t, "animationState"), p = ce(t, "clearCardCss", 7, !1);
  let h = /* @__PURE__ */ H(void 0), c = /* @__PURE__ */ H(!0), d = /* @__PURE__ */ H(0);
  const v = JSON.parse(JSON.stringify(i()));
  Kt(() => {
    g(h) && (g(h).hass = r());
  }), Kt(() => {
    g(h) && (g(h).preview = s());
  }), Kt(() => {
    var _;
    g(h) && (v.disabled = !l(), (_ = g(h)._element) == null || _.dispatchEvent(new CustomEvent("card-visibility-changed")));
  }), Wr(async () => {
    const _ = document.createElement("hui-card");
    _.hass = r(), _.preview = s(), v.disabled = !l(), _.config = v, _.load(), g(h) && (p() && (_.style.setProperty("--ha-card-background", "transparent"), _.style.setProperty("--ha-card-box-shadow", "none"), _.style.setProperty("--ha-card-border-color", "transparent"), _.style.setProperty("--ha-card-border-width", "0px"), _.style.setProperty("--ha-card-border-radius", "0px"), _.style.setProperty("--ha-card-backdrop-filter", "none")), o() && new ResizeObserver((Z) => {
      for (const I of Z)
        if (I.contentBoxSize) {
          const V = Array.isArray(I.contentBoxSize) ? I.contentBoxSize[0] : I.contentBoxSize;
          O(d, V.blockSize || g(d), !0);
        } else
          O(d, I.contentRect.height || g(d), !0);
    }).observe(_), g(h).replaceWith(_), O(h, _, !0), O(c, !1));
  });
  var m = {
    get type() {
      return n();
    },
    set type(_ = "div") {
      n(_), ae();
    },
    get config() {
      return i();
    },
    set config(_) {
      i(_), ae();
    },
    get hass() {
      return r();
    },
    set hass(_) {
      r(_), ae();
    },
    get preview() {
      return s();
    },
    set preview(_) {
      s(_), ae();
    },
    get marginTop() {
      return a();
    },
    set marginTop(_ = "0px") {
      a(_), ae();
    },
    get open() {
      return l();
    },
    set open(_) {
      l(_), ae();
    },
    get animation() {
      return o();
    },
    set animation(_ = !0) {
      o(_), ae();
    },
    get animationState() {
      return f();
    },
    set animationState(_) {
      f(_), ae();
    },
    get clearCardCss() {
      return p();
    },
    set clearCardCss(_ = !1) {
      p(_), ae();
    }
  }, y = qs(), N = Me(y);
  ms(N, n, !1, (_, q) => {
    xs(_, (Z) => O(h, Z, !0), () => g(h)), me(_, 0, "svelte-lv9s7p");
  });
  var C = Gt(N, 2);
  {
    var T = (_) => {
      var q = Cs();
      je(_, q);
    };
    Ot(C, (_) => {
      g(c) && _(T);
    });
  }
  return Ne(y), ze(() => {
    me(y, 1, `outer-container${l() ? " open" : " close"} ${f() ?? ""} ${o() ? "animation" : ""}`, "svelte-lv9s7p"), De(y, `margin-top: ${(l() ? a() : "0px") ?? ""};${g(d) ? ` --expander-animation-height: -${g(d)}px;` : ""}`);
  }), je(e, y), Bn(m);
}
customElements.define("expander-sub-card", Zr(
  On,
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
const An = {
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
var As = /* @__PURE__ */ vt('<button aria-label="Toggle button"><ha-icon></ha-icon></button>', 2), Ns = /* @__PURE__ */ vt('<div id="id1"><div id="id2" class="title-card-container svelte-1jqiztq"><!></div> <!></div>'), Rs = /* @__PURE__ */ vt("<button><div> </div> <ha-icon></ha-icon></button>", 2), js = /* @__PURE__ */ vt("<div><div></div></div>"), Is = /* @__PURE__ */ vt("<ha-card><!> <!></ha-card>", 2);
const Ps = {
  hash: "svelte-1jqiztq",
  code: `.expander-card.svelte-1jqiztq {display:var(--expander-card-display,block);gap:var(--gap);padding:var(--padding);background:var(--card-background,#fff);}.expander-card.animation.svelte-1jqiztq {transition:gap 0.35s ease;}.children-wrapper.svelte-1jqiztq {display:flex;flex-direction:column;}.children-wrapper.animation.opening.svelte-1jqiztq,
    .children-wrapper.animation.closing.svelte-1jqiztq {overflow:hidden;}.children-container.animation.svelte-1jqiztq {transition:padding 0.35s ease, gap 0.35s ease;}.children-container.svelte-1jqiztq {padding:var(--child-padding);display:var(--expander-card-display,block);gap:var(--gap);}.clear.svelte-1jqiztq {background:none !important;background-color:transparent !important;border-style:none !important;}.title-card-header.svelte-1jqiztq {display:flex;align-items:center;justify-content:space-between;flex-direction:row;}.title-card-header-overlay.svelte-1jqiztq {display:block;}.title-card-container.svelte-1jqiztq {width:100%;padding:var(--title-padding);}.header.svelte-1jqiztq {display:flex;flex-direction:row;align-items:center;padding:0.8em 0.8em;margin:2px;background:var(--button-background);border-style:none;width:var(--header-width,auto);color:var(--header-color,#fff);}.header-overlay.svelte-1jqiztq {position:absolute;top:0;right:0;margin:var(--overlay-margin);}.title.svelte-1jqiztq {width:100%;text-align:left;}.ico.animation.svelte-1jqiztq {transition-property:transform;transition-duration:0.35s;}.ico.svelte-1jqiztq {color:var(--arrow-color,var(--primary-text-color,#fff));}.flipped.svelte-1jqiztq {transform:rotate(var(--icon-rotate-degree,180deg));}.ripple.svelte-1jqiztq {background-position:center;transition:background 0.8s;border-radius:1em;}.ripple.svelte-1jqiztq:hover {background:#ffffff12 radial-gradient(circle, transparent 1%, #ffffff12 1%) center/15000%;}.ripple.svelte-1jqiztq:active {background-color:#ffffff25;background-size:100%;transition:background 0s;}`
};
function Ms(e, t) {
  var Lt, Ft;
  Fn(t, !0), Xr(e, Ps);
  const n = ce(t, "hass"), i = ce(t, "preview"), r = ce(t, "config", 7, An);
  let s = /* @__PURE__ */ H(!1), a = /* @__PURE__ */ H(!1), l = /* @__PURE__ */ H("idle"), o = /* @__PURE__ */ H(null);
  const f = r()["storage-id"] ?? r()["storgage-id"], p = "expander-open-" + f, h = r()["show-button-users"] === void 0 || ((Ft = r()["show-button-users"]) == null ? void 0 : Ft.includes((Lt = n()) == null ? void 0 : Lt.user.name));
  function c() {
    g(o) && (clearTimeout(g(o)), O(o, null));
    const b = !g(a);
    r().animation ? (O(l, b ? "opening" : "closing", !0), b ? (d(!0), O(
      o,
      setTimeout(
        () => {
          O(l, "idle"), O(o, null);
        },
        350
      ),
      !0
    )) : O(
      o,
      setTimeout(
        () => {
          d(!1), O(l, "idle"), O(o, null);
        },
        350
      ),
      !0
    )) : d(b);
  }
  function d(b) {
    if (O(a, b, !0), f !== void 0)
      try {
        localStorage.setItem(p, g(a) ? "true" : "false");
      } catch (A) {
        console.error(A);
      }
  }
  Wr(() => {
    var be, ge;
    const b = r()["min-width-expanded"], A = r()["max-width-expanded"], R = document.body.offsetWidth;
    if (b && A ? r().expanded = R >= b && R <= A : b ? r().expanded = R >= b : A && (r().expanded = R <= A), (ge = r()["start-expanded-users"]) != null && ge.includes((be = n()) == null ? void 0 : be.user.name))
      d(!0);
    else if (f !== void 0)
      try {
        const B = localStorage.getItem(p);
        B === null ? r().expanded !== void 0 && d(r().expanded) : O(a, B ? B === "true" : g(a), !0);
      } catch (B) {
        console.error(B);
      }
    else
      r().expanded !== void 0 && d(r().expanded);
  });
  const v = (b) => {
    if (g(s))
      return b.preventDefault(), b.stopImmediatePropagation(), O(s, !1), !1;
    c();
  }, m = (b) => {
    const A = b.currentTarget;
    A != null && A.classList.contains("title-card-container") && v(b);
  };
  let y, N = !1, C = 0, T = 0;
  const _ = (b) => {
    y = b.target, C = b.touches[0].clientX, T = b.touches[0].clientY, N = !1;
  }, q = (b) => {
    const A = b.touches[0].clientX, R = b.touches[0].clientY;
    (Math.abs(A - C) > 10 || Math.abs(R - T) > 10) && (N = !0);
  }, Z = (b) => {
    !N && y === b.target && r()["title-card-clickable"] && c(), y = void 0, O(s, !0);
  };
  var I = {
    get hass() {
      return n();
    },
    set hass(b) {
      n(b), ae();
    },
    get preview() {
      return i();
    },
    set preview(b) {
      i(b), ae();
    },
    get config() {
      return r();
    },
    set config(b = An) {
      r(b), ae();
    }
  }, V = Is(), Q = Me(V);
  {
    var ht = (b) => {
      var A = Ns(), R = Me(A);
      R.__touchstart = _, R.__touchmove = q, R.__touchend = Z, R.__click = function(...ee) {
        var re;
        (re = r()["title-card-clickable"] ? m : null) == null || re.apply(this, ee);
      };
      var be = Me(R);
      {
        let ee = /* @__PURE__ */ Yt(() => r()["clear-children"] || !1);
        On(be, {
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
            return g(ee);
          }
        });
      }
      Ne(R);
      var ge = Gt(R, 2);
      {
        var B = (ee) => {
          var re = As();
          re.__click = v;
          var Ke = Me(re);
          ze(() => nr(Ke, "icon", r().icon)), Ne(re), ze(() => {
            De(re, `--overlay-margin:${r()["overlay-margin"] ?? ""}; --button-background:${r()["button-background"] ?? ""}; --header-color:${r()["header-color"] ?? ""};`), me(re, 1, `header ripple${r()["title-card-button-overlay"] ? " header-overlay" : ""}${g(a) ? " open" : " close"}`, "svelte-1jqiztq"), De(Ke, `--arrow-color:${r()["arrow-color"] ?? ""}`), me(Ke, 1, `ico${g(a) && g(l) !== "closing" ? " flipped open" : " close"} ${r().animation ? "animation" : ""}`, "svelte-1jqiztq");
          }), je(ee, re);
        };
        Ot(ge, (ee) => {
          h && ee(B);
        });
      }
      Ne(A), ze(() => {
        me(A, 1, `title-card-header${r()["title-card-button-overlay"] ? "-overlay" : ""}`, "svelte-1jqiztq"), De(R, `--title-padding:${r()["title-card-padding"] ?? ""}`), Gr(R, "role", r()["title-card-clickable"] ? "button" : void 0);
      }), je(b, A);
    }, Xe = (b) => {
      var A = ls(), R = Ui(A);
      {
        var be = (ge) => {
          var B = Rs();
          B.__click = v;
          var ee = Me(B), re = Me(ee, !0);
          Ne(ee);
          var Ke = Gt(ee, 2);
          ze(() => nr(Ke, "icon", r().icon)), Ne(B), ze(() => {
            me(B, 1, `header${r()["expander-card-background-expanded"] ? "" : " ripple"}${g(a) ? " open" : " close"}`, "svelte-1jqiztq"), De(B, `--header-width:100%; --button-background:${r()["button-background"] ?? ""};--header-color:${r()["header-color"] ?? ""};`), me(ee, 1, `primary title${g(a) ? " open" : " close"}`, "svelte-1jqiztq"), ds(re, r().title), De(Ke, `--arrow-color:${r()["arrow-color"] ?? ""}`), me(Ke, 1, `ico${g(a) && g(l) !== "closing" ? " flipped open" : " close"} ${r().animation ? "animation" : ""}`, "svelte-1jqiztq");
          }), je(ge, B);
        };
        Ot(R, (ge) => {
          h && ge(be);
        });
      }
      je(b, A);
    };
    Ot(Q, (b) => {
      r()["title-card"] ? b(ht) : b(Xe, !1);
    });
  }
  var Ge = Gt(Q, 2);
  {
    var pn = (b) => {
      var A = js(), R = Me(A);
      _s(R, 20, () => r().cards, (be) => be, (be, ge) => {
        {
          let B = /* @__PURE__ */ Yt(() => g(a) && i()), ee = /* @__PURE__ */ Yt(() => r().animation || !1), re = /* @__PURE__ */ Yt(() => r()["clear-children"] || !1);
          On(be, {
            get hass() {
              return n();
            },
            get preview() {
              return g(B);
            },
            get config() {
              return ge;
            },
            get type() {
              return ge.type;
            },
            get marginTop() {
              return r()["child-margin-top"];
            },
            get open() {
              return g(a);
            },
            get animation() {
              return g(ee);
            },
            get animationState() {
              return g(l);
            },
            get clearCardCss() {
              return g(re);
            }
          });
        }
      }), Ne(R), Ne(A), ze(() => {
        me(A, 1, `children-wrapper ${r().animation ? "animation " + g(l) : ""}`, "svelte-1jqiztq"), De(R, `--expander-card-display:${r()["expander-card-display"] ?? ""};
                --gap:${(g(a) && g(l) !== "closing" ? r()["expanded-gap"] : r().gap) ?? ""};
                --child-padding:${(g(a) && g(l) !== "closing" ? r()["child-padding"] : "0px") ?? ""};`), me(R, 1, `children-container${g(a) ? " open" : " close"} ${g(l) ?? ""} ${r().animation ? "animation" : ""}`, "svelte-1jqiztq");
      }), je(b, A);
    };
    Ot(Ge, (b) => {
      r().cards && b(pn);
    });
  }
  return Ne(V), ze(() => {
    me(V, 1, `expander-card${r().clear ? " clear" : ""}${g(a) ? " open" : " close"} ${g(l)} ${r().animation ? "animation" : ""}`, "svelte-1jqiztq"), De(V, `--expander-card-display:${r()["expander-card-display"] ?? ""};
     --gap:${(g(a) && g(l) !== "closing" ? r()["expanded-gap"] : r().gap) ?? ""}; --padding:${r().padding ?? ""};
     --expander-state:${g(a) ?? ""};
     --icon-rotate-degree:${r()["icon-rotate-degree"] ?? ""};
     --card-background:${(g(a) && r()["expander-card-background-expanded"] ? r()["expander-card-background-expanded"] : r()["expander-card-background"]) ?? ""}
    `);
  }), je(e, V), Bn(I);
}
ss(["touchstart", "touchmove", "touchend", "click"]);
customElements.define("expander-card", Zr(Ms, { hass: {}, preview: {}, config: {} }, [], [], !0, (e) => class extends e {
  constructor() {
    super(...arguments);
    // re-declare props used in customClass.
    M(this, "config");
  }
  setConfig(n = {}) {
    this.config = { ...An, ...n };
  }
}));
const zs = "2.9.3";
console.info(
  `%c  Expander-Card 
%c Version ${zs}`,
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
  Ms as default
};
//# sourceMappingURL=expander-card.js.map
