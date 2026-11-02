"""Trajectory evaluation component of the proposed event-based VO benchmarking framework.

Implements least-squares trajectory alignment (Umeyama, 1991) in rigid SE(3) and
similarity Sim(3) form, absolute trajectory error (ATE) and a translation-only
relative pose error (RPE) over a fixed sample interval.
"""

import numpy as np


def generate_ground_truth(n_samples=1800, duration_s=25.0):
    """Smooth 3D reference path with horizontal curves and varying height (metres)."""
    t = np.linspace(0.0, duration_s, n_samples)
    x = 3.0 * np.cos(0.25 * t) + 0.5 * t
    y = 2.0 * np.sin(0.5 * t)
    z = 1.0 + 0.3 * np.sin(0.4 * t)
    return t, np.column_stack([x, y, z])


def rotation_from_euler(roll_deg, pitch_deg, yaw_deg):
    r, p, y = np.radians([roll_deg, pitch_deg, yaw_deg])
    rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
    ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
    rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
    return rz @ ry @ rx


# Fixed frame change used for every estimated trajectory
FRAME_ROTATION = rotation_from_euler(5.0, 10.0, 30.0)
FRAME_TRANSLATION = np.array([2.0, -1.0, 0.5])


def to_estimate_frame(positions):
    return positions @ FRAME_ROTATION.T + FRAME_TRANSLATION


def align(estimate, reference, with_scale):
    """Return (scale, R, t) minimising ||reference - (scale * R @ estimate + t)||."""
    mu_e = estimate.mean(axis=0)
    mu_r = reference.mean(axis=0)
    e = estimate - mu_e
    r = reference - mu_r
    cov = r.T @ e / len(estimate)
    u, d, vt = np.linalg.svd(cov)
    s_fix = np.eye(3)
    if np.linalg.det(u) * np.linalg.det(vt) < 0:
        s_fix[2, 2] = -1.0
    rot = u @ s_fix @ vt
    if with_scale:
        var_e = (e ** 2).sum() / len(estimate)
        scale = np.trace(np.diag(d) @ s_fix) / var_e
    else:
        scale = 1.0
    trans = mu_r - scale * rot @ mu_e
    return scale, rot, trans


def apply(estimate, scale, rot, trans):
    return scale * estimate @ rot.T + trans


def ate_rmse(aligned, reference):
    return float(np.sqrt(np.mean(np.sum((aligned - reference) ** 2, axis=1))))


def rpe_translation_rmse(aligned, reference, interval=10):
    d_est = aligned[interval:] - aligned[:-interval]
    d_ref = reference[interval:] - reference[:-interval]
    return float(np.sqrt(np.mean(np.sum((d_est - d_ref) ** 2, axis=1))))


def evaluate(estimate, reference, mode, interval=10):
    """Align estimate to reference with 'SE3' or 'Sim3' and return metrics."""
    scale, rot, trans = align(estimate, reference, with_scale=(mode == "Sim3"))
    aligned = apply(estimate, scale, rot, trans)
    return {
        "ate_rmse_m": ate_rmse(aligned, reference),
        "rpe_rmse_m": rpe_translation_rmse(aligned, reference, interval),
        "fitted_scale": float(scale),
    }
