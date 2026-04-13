from __future__ import annotations

import numpy as np
from typing import List, Tuple


class MathService:
    """
    Centralized numerical and linear algebra utilities.

    Designed for:
    - Geometry transformations
    - Energy computations
    - DNA structural modeling
    """

    # =========================
    # Basic Vector Operations
    # =========================

    @staticmethod
    def to_array(vec: List[float]) -> np.ndarray:
        return np.asarray(vec, dtype=float)

    @staticmethod
    def norm(vec: np.ndarray) -> float:
        return float(np.linalg.norm(vec))

    @staticmethod
    def normalize(vec: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(vec)
        if norm == 0:
            raise ValueError("Cannot normalize zero vector")
        return vec / norm

    @staticmethod
    def dot(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b))

    @staticmethod
    def cross(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.cross(a, b)

    # =========================
    # Matrix Operations
    # =========================

    @staticmethod
    def matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.matmul(a, b)

    @staticmethod
    def transpose(m: np.ndarray) -> np.ndarray:
        return m.T

    @staticmethod
    def inverse(m: np.ndarray) -> np.ndarray:
        if m.shape[0] != m.shape[1]:
            raise ValueError("Matrix must be square")
        return np.linalg.inv(m)

    @staticmethod
    def identity(n: int = 3) -> np.ndarray:
        return np.eye(n)

    # =========================
    # Rotation Utilities
    # =========================

    @staticmethod
    def rotation_x(theta: float) -> np.ndarray:
        c, s = np.cos(theta), np.sin(theta)
        return np.array([
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ])

    @staticmethod
    def rotation_y(theta: float) -> np.ndarray:
        c, s = np.cos(theta), np.sin(theta)
        return np.array([
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ])

    @staticmethod
    def rotation_z(theta: float) -> np.ndarray:
        c, s = np.cos(theta), np.sin(theta)
        return np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])

    # =========================
    # Rodrigues Rotation
    # =========================

    @staticmethod
    def rodrigues(axis: np.ndarray, theta: float) -> np.ndarray:
        """
        Rodrigues rotation formula.
        """
        axis = MathService.normalize(axis)

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

    @staticmethod
    def apply_transform(
        position: np.ndarray,
        rotation: np.ndarray,
        vector: np.ndarray
    ) -> np.ndarray:
        """
        Applies rotation + translation.
        """
        return position + rotation @ vector

    @staticmethod
    def compose_transform(
        pos1: np.ndarray,
        rot1: np.ndarray,
        pos2: np.ndarray,
        rot2: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compose two transformations.
        """
        new_pos = pos1 + rot1 @ pos2
        new_rot = rot1 @ rot2

        return new_pos, new_rot

    # =========================
    # Batch Operations
    # =========================

    @staticmethod
    def batch_matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """
        Batch matrix multiplication.
        Shape: (N,3,3)
        """
        return np.einsum("nij,njk->nik", A, B)

    @staticmethod
    def batch_dot(A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """
        Batch dot product.
        """
        return np.einsum("ij,ij->i", A, B)

    # =========================
    # Energy Utilities
    # =========================

    @staticmethod
    def quadratic_form(vec: np.ndarray, matrix: np.ndarray) -> float:
        """
        Computes 0.5 * v^T K v
        """
        return float(0.5 * vec.T @ matrix @ vec)

    @staticmethod
    def batch_quadratic_form(
        vectors: np.ndarray,
        matrix: np.ndarray
    ) -> np.ndarray:
        """
        Efficient batch energy computation.
        """
        return 0.5 * np.einsum("ij,jk,ik->i", vectors, matrix, vectors)

    # =========================
    # Validation Utilities
    # =========================

    @staticmethod
    def validate_vector(vec: np.ndarray, size: int):
        if vec.shape != (size,):
            raise ValueError(f"Vector must have shape ({size},)")

    @staticmethod
    def validate_matrix(mat: np.ndarray, shape: Tuple[int, int]):
        if mat.shape != shape:
            raise ValueError(f"Matrix must have shape {shape}")
