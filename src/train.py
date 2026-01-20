"""
Training Script for Azure ML

This script runs on Azure ML Compute and trains an ML model.
It accepts command-line arguments and uses MLflow for tracking.
"""

import argparse
import os
from pathlib import Path

import mlflow
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Train a Random Forest model on Iris dataset"
    )
    
    parser.add_argument(
        "--n_estimators",
        type=int,
        default=100,
        help="Number of trees in random forest"
    )
    
    parser.add_argument(
        "--max_depth",
        type=int,
        default=5,
        help="Maximum depth of trees"
    )
    
    parser.add_argument(
        "--test_size",
        type=float,
        default=0.2,
        help="Proportion of dataset to include in test split"
    )
    
    parser.add_argument(
        "--random_state",
        type=int,
        default=42,
        help="Random state for reproducibility"
    )
    
    return parser.parse_args()


def load_data():
    """Load and prepare the Iris dataset."""
    print("Loading Iris dataset...")
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='target')
    
    print(f"Dataset shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    return X, y


def train_model(X_train, y_train, n_estimators, max_depth, random_state):
    """Train a Random Forest classifier."""
    print(f"\nTraining Random Forest with:")
    print(f"  n_estimators: {n_estimators}")
    print(f"  max_depth: {max_depth}")
    print(f"  random_state: {random_state}")
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )
    
    model.fit(X_train, y_train)
    print("Training completed!")
    
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate the trained model."""
    print("\nEvaluating model...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return accuracy, y_pred


def main():
    """Main training function."""
    # Parse arguments
    args = parse_args()
    
    print("="*60)
    print("Azure ML Training Job - Iris Classification")
    print("="*60)
    
    # Start MLflow run
    mlflow.start_run()
    
    # Log parameters
    mlflow.log_param("n_estimators", args.n_estimators)
    mlflow.log_param("max_depth", args.max_depth)
    mlflow.log_param("test_size", args.test_size)
    mlflow.log_param("random_state", args.random_state)
    
    # Load data
    X, y = load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y
    )
    
    print(f"\nTrain set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train model
    model = train_model(
        X_train, y_train,
        args.n_estimators,
        args.max_depth,
        args.random_state
    )
    
    # Evaluate model
    accuracy, y_pred = evaluate_model(model, X_test, y_test)
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="iris_random_forest"
    )
    
    print("\n" + "="*60)
    print("Training completed successfully!")
    print(f"Model logged to MLflow with accuracy: {accuracy:.4f}")
    print("="*60)
    
    mlflow.end_run()


if __name__ == "__main__":
    main()
