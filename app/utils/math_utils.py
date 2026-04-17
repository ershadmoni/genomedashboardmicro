from __future__ import annotations

import numpy as np
from typing import Tuple


# =========================
# Vector Utilities
# =========================

def norm(vec: np.ndarray) -> float:
    return float(np.linalg.norm(vec))


def normalize(vec: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(vec)
    if n == 0:
        raise ValueError("Cannot normalize zero vector")
    return vec / n


def dot(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def cross(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.cross(a, b)


# =========================
# Matrix Utilities
# =========================

def identity(n: int = 3) -> np.ndarray:
    return np.eye(n)


def transpose(m: np.ndarray) -> np.ndarray:
    return m.T


def inverse(m: np.ndarray) -> np.ndarray:
    if m.shape[0] != m.shape[1]:
        raise ValueError("Matrix must be square")
    return np.linalg.inv(m)


def matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.matmul(a, b)


# =========================
# Rotation Matrices
# =========================

def rotation_x(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])


def rotation_y(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])


def rotation_z(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])


# =========================
# Rodrigues Formula
# =========================

def rodrigues(axis: np.ndarray, theta: float) -> np.ndarray:
    """
    Rodrigues rotation formula for arbitrary axis rotation.
    """
    axis = normalize(axis)

    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])

    I = np.eye(3)

    return I + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)


# =========================
# Transformation Utilities
# =========================

def apply_transform(
    position: np.ndarray,
    rotation: np.ndarray,
    vector: np.ndarray
) -> np.ndarray:
    """
    Apply rotation + translation.
    """
    return position + rotation @ vector


def compose_transform(
    pos1: np.ndarray,
    rot1: np.ndarray,
    pos2: np.ndarray,
    rot2: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Combine two rigid transformations.
    """
    new_pos = pos1 + rot1 @ pos2
    new_rot = rot1 @ rot2

    return new_pos, new_rot


# =========================
# Batch Operations
# =========================

def batch_matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Batch matrix multiplication.
    Shape: (N,3,3)
    """
    return np.einsum("nij,njk->nik", A, B)


def batch_dot(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Batch dot product.
    """
    return np.einsum("ij,ij->i", A, B)


# =========================
# Energy Utilities
# =========================

def quadratic_form(vec: np.ndarray, K: np.ndarray) -> float:
    """
    Compute 0.5 * v^T K v
    """
    return float(0.5 * vec.T @ K @ vec)


def batch_quadratic_form(
    vectors: np.ndarray,
    K: np.ndarray
) -> np.ndarray:
    """
    Compute energy for multiple vectors efficiently.
    """
    return 0.5 * np.einsum("ij,jk,ik->i", vectors, K, vectors)


# =========================
# Numerical Stability
# =========================

def safe_arccos(x: float) -> float:
    """
    Numerical safe arccos.
    """
    return float(np.arccos(np.clip(x, -1.0, 1.0)))


def safe_sqrt(x: float) -> float:
    """
    Avoid negative due to floating-point errors.
    """
    return float(np.sqrt(max(x, 0.0)))


# =========================
# Validation Utilities
# =========================

def validate_vector(vec: np.ndarray, size: int) -> None:
    if vec.shape != (size,):
        raise ValueError(f"Expected vector shape ({size},), got {vec.shape}")


def validate_matrix(mat: np.ndarray, shape: Tuple[int, int]) -> None:
    if mat.shape != shape:
        raise ValueError(f"Expected matrix shape {shape}, got {mat.shape}")
