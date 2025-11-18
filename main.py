import cv2
import numpy as np
import os
import glob


def extraire_texture_gabor(image_path, ksize=31, sigma=4.0, theta=np.pi / 4, lambd=10.0, gamma=0.5):
    """
    Charge une image, la convertit en niveaux de gris et applique un filtre de Gabor
    pour l'extraction de texture.

    Args:
        image_path (str): Chemin complet vers le fichier image (par exemple, frag_eroded_0000.ppm).
        ksize (int): Taille du noyau du filtre (doit être impair).
        sigma (float): Écart-type du gaussien.
        theta (float): Orientation du filtre (en radians). Ex: np.pi/4 pour 45 degrés.
        lambd (float): Longueur d'onde de la sinusoïde.
        gamma (float): Rapport d'aspect spatial (gamma).

    Returns:
        tuple: (nom_fichier, image_filtrée_texture), où image_filtrée_texture est l'image
               résultante après application du filtre de Gabor.
    """
    try:
        # 1. Chargement de l'image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Erreur: Impossible de charger l'image {image_path}. Vérifiez le chemin.")
            return os.path.basename(image_path), None

        # 2. Convertir en niveaux de gris (essentiel pour la plupart des traitements de texture)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Créer et appliquer le filtre de Gabor
        # Gabor est excellent pour détecter des orientations et des fréquences spécifiques (texture)
        kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, 0, ktype=cv2.CV_32F)
        filtered_image = cv2.filter2D(gray, cv2.CV_8UC3, kernel)

        return os.path.basename(image_path), filtered_image

    except Exception as e:
        print(f"Une erreur est survenue lors du traitement de {image_path}: {e}")
        return os.path.basename(image_path), None


def balayer_et_traiter_images(repertoire_racine):
    chemin_recherche = os.path.join(repertoire_racine, 'frag_eroded_*.ppm')

    image_files = sorted(glob.glob(chemin_recherche))

    if not image_files:
        print(f"Aucune image '.ppm' trouvée dans le répertoire: {repertoire_racine}")
        return

    print(f"Démarrage du traitement de {len(image_files)} images...")

    gabor_params = {
        'ksize': 31,
        'sigma': 5.0,
        'theta': np.pi / 4,
        'lambd': 10.0,
        'gamma': 0.5
    }
    # --------------------------------------

    for image_path in image_files:
        nom_fichier, texture_image = extraire_texture_gabor(image_path, **gabor_params)

        if texture_image is not None:
            print(f"Texture extraite de **{nom_fichier}** (forme: {texture_image.shape})")

            # Afficher l'image traitée (décommenter si vous exécutez le script localement avec une interface graphique)
            # cv2.imshow(f"Original - {nom_fichier}", cv2.imread(image_path))
            # cv2.imshow(f"Texture Gabor - {nom_fichier}", texture_image)
            # cv2.waitKey(500) # Attendre 500 ms pour l'affichage de chaque image

            # --- Enregistrement de l'image traitée (Optionnel) ---
            repertoire_sortie = os.path.join(repertoire_racine, 'textures_traitees')
            os.makedirs(repertoire_sortie, exist_ok=True)
            nom_sortie = f"texture_{nom_fichier.replace('.ppm', '.png')}"
            cv2.imwrite(os.path.join(repertoire_sortie, nom_sortie), texture_image)
            print(f"Image de texture enregistrée: {os.path.join(repertoire_sortie, nom_sortie)}")

    # cv2.destroyAllWindows() # Ferme toutes les fenêtres d'affichage à la fin (si affichage activé)
    print("\nTraitement terminé.")


REPERTOIRE_IMAGES = r"C:\Users\aliam\OneDrive\Desktop\6fresques_et\6fresques_et\Lanzani_SantAntonioproteggePavia_2440x2524\frag_eroded"

# Exécution de la fonction principale
balayer_et_traiter_images(REPERTOIRE_IMAGES)