"""
Script de test pour l'API de prédiction de défaut de crédit
"""
import requests
import json

# URL de l'API (ajustez selon votre configuration)
API_URL = "http://localhost:8000"

def test_health_check():
    """Test de l'endpoint de santé"""
    print("=" * 50)
    print("Test de l'endpoint de santé...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_root():
    """Test de l'endpoint racine"""
    print("=" * 50)
    print("Test de l'endpoint racine...")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_predict():
    """Test de l'endpoint de prédiction avec des données d'exemple"""
    print("=" * 50)
    print("Test de l'endpoint de prédiction...")
    
    # Données d'exemple pour un client
    test_data = {
        "LIMIT_BAL": 20000.0,
        "SEX": 2,  # 1=male, 2=female
        "EDUCATION": 2,  # 1=graduate school, 2=university, 3=high school, 4=others
        "MARRIAGE": 1,  # 1=married, 2=single, 3=others
        "AGE": 24,
        "PAY_0": -1,  # -1=pay duly, 1=payment delay for one month, ...
        "PAY_2": 2,
        "PAY_3": 0,
        "PAY_4": 0,
        "PAY_5": -1,
        "PAY_6": -1,
        "BILL_AMT1": 3913.0,
        "BILL_AMT2": 3102.0,
        "BILL_AMT3": 689.0,
        "BILL_AMT4": 0.0,
        "BILL_AMT5": 0.0,
        "BILL_AMT6": 0.0,
        "PAY_AMT1": 0.0,
        "PAY_AMT2": 689.0,
        "PAY_AMT3": 0.0,
        "PAY_AMT4": 0.0,
        "PAY_AMT5": 0.0,
        "PAY_AMT6": 0.0
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Request Data:")
        print(json.dumps(test_data, indent=2))
        print(f"\nResponse:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ Prédiction réussie!")
            print(f"  - Classe prédite: {result.get('prediction')} (0=pas de défaut, 1=défaut)")
            print(f"  - Probabilité de défaut: {result.get('probability_default', 0):.4f} ({result.get('probability_default', 0)*100:.2f}%)")
            return True
        else:
            print(f"✗ Erreur dans la prédiction")
            return False
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def main():
    """Fonction principale pour exécuter tous les tests"""
    print("\n" + "=" * 50)
    print("TESTS DE L'API DE PRÉDICTION DE DÉFAUT DE CRÉDIT")
    print("=" * 50 + "\n")
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Root endpoint
    results.append(("Root Endpoint", test_root()))
    
    # Test 3: Prediction
    results.append(("Prediction", test_predict()))
    
    # Résumé des résultats
    print("\n" + "=" * 50)
    print("RÉSUMÉ DES TESTS")
    print("=" * 50)
    for test_name, result in results:
        status = "✓ PASSÉ" if result else "✗ ÉCHOUÉ"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print("=" * 50)
    if all_passed:
        print("✓ Tous les tests sont passés avec succès!")
    else:
        print("✗ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()

