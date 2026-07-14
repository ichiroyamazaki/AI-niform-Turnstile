import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import json
from ultralytics import YOLO
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops
from skimage.color import rgb2gray
import hashlib
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniformAnnotator:
    """Automatic uniform annotation and uniqueness detection system"""
    
    def __init__(self, model_path: str = "yolov8n.pt"):
        """Initialize the annotator with YOLO model"""
        try:
            self.model = YOLO(model_path)
            logger.info(f"✅ YOLO model loaded from {model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load YOLO model: {e}")
            self.model = None
        
        # Define uniform-specific classes (can be customized)
        self.uniform_classes = {
            0: 'polo_shirt',
            1: 't_shirt', 
            2: 'blouse',
            3: 'pants',
            4: 'skirt',
            5: 'dress',
            6: 'jacket',
            7: 'shoes',
            8: 'accessory'
        }
        
        # Initialize feature extraction parameters
        self.lbp_radius = 3
        self.lbp_n_points = 8
        self.glcm_distances = [1, 2, 3]
        self.glcm_angles = [0, 45, 90, 135]
    
    def annotate_uniform(self, image_path: str) -> Dict:
        """
        Automatically annotate a uniform image with detection and features
        
        Args:
            image_path: Path to the uniform image
            
        Returns:
            Dictionary containing annotation data
        """
        try:
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert BGR to RGB for PIL
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            
            # STEP 1: Analyze uniform structure and detect clothing items
            detection_results = self._detect_uniform_components(image_path)
            
            # STEP 2: Extract uniform-specific features
            uniform_features = self._extract_uniform_features(image)
            
            # STEP 3: Analyze logos and emblems
            logo_analysis = self._analyze_logos_and_emblems(image)
            
            # STEP 4: Extract color schemes and patterns
            color_analysis = self._analyze_uniform_colors(image)
            
            # STEP 5: Detect text and insignias
            text_analysis = self._detect_text_and_insignias(image)
            
            # STEP 6: Generate comprehensive uniqueness signature
            uniqueness_signature = self._generate_uniform_uniqueness_signature(
                image, uniform_features, logo_analysis, color_analysis, text_analysis
            )
            
            # Create comprehensive annotation data
            annotation_data = {
                'image_path': image_path,
                'image_dimensions': {
                    'width': image.shape[1],
                    'height': image.shape[0],
                    'channels': image.shape[2]
                },
                'detection_results': detection_results,
                'uniform_features': uniform_features,
                'logo_analysis': logo_analysis,
                'color_analysis': color_analysis,
                'text_analysis': text_analysis,
                'uniqueness_signature': uniqueness_signature,
                'annotation_timestamp': datetime.now().isoformat(),
                'annotation_version': '2.0'
            }
            
            logger.info(f"✅ Successfully annotated uniform image: {image_path}")
            return annotation_data
            
        except Exception as e:
            logger.error(f"❌ Failed to annotate uniform: {e}")
            return {
                'error': str(e),
                'image_path': image_path,
                'annotation_timestamp': datetime.now().isoformat()
            }
    
    def _detect_uniform_components(self, image_path: str) -> Dict:
        """Detect uniform components and clothing items using YOLO"""
        if not self.model:
            return {'error': 'YOLO model not available'}
        
        try:
            # Run YOLO detection
            results = self.model(image_path)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        
                        # Get confidence and class
                        confidence = float(box.conf[0].cpu().numpy())
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = self.uniform_classes.get(class_id, f'unknown_{class_id}')
                        
                        if confidence > 0.5:  # Filter by confidence threshold
                            detections.append({
                                'class_id': class_id,
                                'class_name': class_name,
                                'confidence': confidence,
                                'bbox': {
                                    'x1': float(x1),
                                    'y1': float(y1),
                                    'x2': float(x2),
                                    'y2': float(y2)
                                },
                                'area': float((x2 - x1) * (y2 - y1))
                            })
            
            return {
                'total_detections': len(detections),
                'detections': detections,
                'detection_model': 'YOLOv8n'
            }
            
        except Exception as e:
            logger.error(f"❌ Uniform component detection failed: {e}")
            return {'error': str(e)}
    
    def _extract_uniform_features(self, image: np.ndarray) -> Dict:
        """Extract uniform-specific features including fabric texture and patterns"""
        try:
            # Convert to grayscale for texture analysis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Fabric texture analysis using LBP
            lbp = local_binary_pattern(gray, self.lbp_n_points, self.lbp_radius, method='uniform')
            lbp_hist, _ = np.histogram(lbp, bins=10, range=(0, 10), density=True)
            
            # Pattern detection using edge analysis
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            # Fabric smoothness analysis
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
            fabric_smoothness = 1.0 / (1.0 + np.mean(gradient_magnitude))
            
            return {
                'fabric_texture_lbp': lbp_hist.tolist(),
                'pattern_edge_density': float(edge_density),
                'fabric_smoothness': float(fabric_smoothness),
                'texture_complexity': float(np.std(gradient_magnitude))
            }
            
        except Exception as e:
            logger.error(f"❌ Uniform feature extraction failed: {e}")
            return {'error': str(e)}
    
    def _analyze_logos_and_emblems(self, image: np.ndarray) -> Dict:
        """Analyze logos, emblems, and distinctive symbols on uniforms"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Logo detection using contour analysis
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            logo_candidates = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if 100 < area < 10000:  # Filter by size
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    # Look for roughly circular or square shapes (typical for logos)
                    if 0.5 < aspect_ratio < 2.0:
                        logo_candidates.append({
                            'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                            'area': float(area),
                            'aspect_ratio': float(aspect_ratio),
                            'center': {'x': int(x + w/2), 'y': int(y + h/2)}
                        })
            
            # Analyze logo regions for distinctiveness
            logo_features = []
            for candidate in logo_candidates[:5]:  # Top 5 candidates
                x, y, w, h = candidate['bbox']['x'], candidate['bbox']['y'], candidate['bbox']['width'], candidate['bbox']['height']
                roi = gray[y:y+h, x:x+w]
                
                if roi.size > 0:
                    # Calculate distinctiveness (contrast with surrounding area)
                    surrounding = gray[max(0, y-10):min(gray.shape[0], y+h+10), 
                                    max(0, x-10):min(gray.shape[1], x+w+10)]
                    if surrounding.size > 0:
                        contrast = np.std(roi) / (np.std(surrounding) + 1e-6)
                        candidate['distinctiveness'] = float(contrast)
                        logo_features.append(candidate)
            
            return {
                'total_logos': len(logo_features),
                'logo_candidates': logo_features,
                'logo_detection_method': 'contour_analysis'
            }
            
        except Exception as e:
            logger.error(f"❌ Logo analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_uniform_colors(self, image: np.ndarray) -> Dict:
        """Analyze uniform color schemes, patterns, and color distribution"""
        try:
            # Convert to different color spaces
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            
            # Primary color analysis
            primary_colors = self._find_dominant_colors(image, 8)
            
            # Color harmony analysis
            color_harmony = self._analyze_color_harmony(hsv)
            
            # Pattern analysis using color distribution
            color_pattern = self._analyze_color_patterns(image)
            
            # Uniform color consistency
            color_consistency = self._analyze_color_consistency(image)
            
            return {
                'primary_colors': primary_colors,
                'color_harmony': color_harmony,
                'color_pattern': color_pattern,
                'color_consistency': color_consistency,
                'color_spaces': {
                    'bgr_means': np.mean(image, axis=(0, 1)).tolist(),
                    'hsv_means': np.mean(hsv, axis=(0, 1)).tolist(),
                    'lab_means': np.mean(lab, axis=(0, 1)).tolist()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Color analysis failed: {e}")
            return {'error': str(e)}
    
    def _detect_text_and_insignias(self, image: np.ndarray) -> Dict:
        """Detect text, numbers, and insignias on uniforms"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Text detection using morphological operations
            # Create a kernel for text detection
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            
            # Apply morphological operations to find text-like regions
            morph = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
            morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
            
            # Find contours that might be text
            _, binary = cv2.threshold(morph, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            text_candidates = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if 50 < area < 5000:  # Filter by size
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    # Text typically has specific aspect ratios
                    if 0.1 < aspect_ratio < 10.0:
                        text_candidates.append({
                            'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                            'area': float(area),
                            'aspect_ratio': float(aspect_ratio),
                            'type': 'potential_text_or_insignia'
                        })
            
            return {
                'total_text_regions': len(text_candidates),
                'text_candidates': text_candidates,
                'detection_method': 'morphological_analysis'
            }
            
        except Exception as e:
            logger.error(f"❌ Text detection failed: {e}")
            return {'error': str(e)}
    
    def _generate_uniform_uniqueness_signature(self, image: np.ndarray, uniform_features: Dict, 
                                             logo_analysis: Dict, color_analysis: Dict, 
                                             text_analysis: Dict) -> str:
        """Generate comprehensive uniqueness signature for uniforms"""
        try:
            # Create feature vector combining all analyses
            features = []
            
            # Add color features
            if 'color_spaces' in color_analysis:
                features.extend(color_analysis['color_spaces']['bgr_means'])
                features.extend(color_analysis['color_spaces']['hsv_means'])
            
            # Add logo features
            if 'total_logos' in logo_analysis:
                features.append(logo_analysis['total_logos'])
                for logo in logo_analysis.get('logo_candidates', [])[:3]:
                    features.extend([logo.get('area', 0), logo.get('aspect_ratio', 0)])
            
            # Add text features
            if 'total_text_regions' in text_analysis:
                features.append(text_analysis['total_text_regions'])
            
            # Add uniform-specific features
            if 'fabric_smoothness' in uniform_features:
                features.append(uniform_features['fabric_smoothness'])
                features.append(uniform_features['texture_complexity'])
            
            # Add edge and texture features
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            features.append(edge_density)
            
            # Convert to string and hash
            feature_string = ','.join([str(f) for f in features])
            signature = hashlib.md5(feature_string.encode()).hexdigest()
            
            return signature
            
        except Exception as e:
            logger.error(f"❌ Uniqueness signature generation failed: {e}")
            return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()
    
    def _analyze_color_harmony(self, hsv_image: np.ndarray) -> Dict:
        """Analyze color harmony and relationships"""
        try:
            # Extract hue and saturation channels
            hue = hsv_image[:, :, 0]
            saturation = hsv_image[:, :, 1]
            
            # Calculate color harmony metrics
            hue_variety = len(np.unique(hue))
            saturation_balance = np.std(saturation)
            
            # Analyze color temperature (warm vs cool)
            warm_colors = np.sum((hue < 30) | (hue > 150))
            cool_colors = np.sum((hue >= 30) & (hue <= 150))
            color_temperature = 'warm' if warm_colors > cool_colors else 'cool'
            
            return {
                'hue_variety': int(hue_variety),
                'saturation_balance': float(saturation_balance),
                'color_temperature': color_temperature,
                'warm_cool_ratio': float(warm_colors / (cool_colors + 1e-6))
            }
            
        except Exception as e:
            logger.error(f"❌ Color harmony analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_color_patterns(self, image: np.ndarray) -> Dict:
        """Analyze color patterns and distribution"""
        try:
            # Calculate color histograms
            bgr_hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            
            # Analyze color distribution
            color_distribution = {
                'total_colors': int(np.sum(bgr_hist > 0)),
                'color_entropy': float(-np.sum(bgr_hist * np.log2(bgr_hist + 1e-10))),
                'dominant_color_ratio': float(np.max(bgr_hist) / np.sum(bgr_hist))
            }
            
            return color_distribution
            
        except Exception as e:
            logger.error(f"❌ Color pattern analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_color_consistency(self, image: np.ndarray) -> Dict:
        """Analyze color consistency across the uniform"""
        try:
            # Split image into regions
            h, w = image.shape[:2]
            regions = [
                image[:h//2, :w//2],      # Top-left
                image[:h//2, w//2:],      # Top-right
                image[h//2:, :w//2],      # Bottom-left
                image[h//2:, w//2:]       # Bottom-right
            ]
            
            # Calculate color consistency between regions
            region_colors = []
            for region in regions:
                if region.size > 0:
                    region_colors.append(np.mean(region, axis=(0, 1)))
            
            if len(region_colors) > 1:
                # Calculate color variation between regions
                color_variation = np.std(region_colors, axis=0)
                consistency_score = 1.0 / (1.0 + np.mean(color_variation))
            else:
                consistency_score = 1.0
            
            return {
                'consistency_score': float(consistency_score),
                'color_variation': float(np.mean(color_variation)) if len(region_colors) > 1 else 0.0,
                'regions_analyzed': len(region_colors)
            }
            
        except Exception as e:
            logger.error(f"❌ Color consistency analysis failed: {e}")
            return {'error': str(e)}
    
    def _detect_objects(self, image_path: str) -> Dict:
        """Detect objects in the image using YOLO"""
        if not self.model:
            return {'error': 'YOLO model not available'}
        
        try:
            # Run YOLO detection
            results = self.model(image_path)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        
                        # Get confidence and class
                        confidence = float(box.conf[0].cpu().numpy())
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = self.uniform_classes.get(class_id, f'unknown_{class_id}')
                        
                        if confidence > 0.5:  # Filter by confidence threshold
                            detections.append({
                                'class_id': class_id,
                                'class_name': class_name,
                                'confidence': confidence,
                                'bbox': {
                                    'x1': float(x1),
                                    'y1': float(y1),
                                    'x2': float(x2),
                                    'y2': float(y2)
                                },
                                'area': float((x2 - x1) * (y2 - y1))
                            })
            
            return {
                'total_detections': len(detections),
                'detections': detections,
                'detection_model': 'YOLOv8n'
            }
            
        except Exception as e:
            logger.error(f"❌ Object detection failed: {e}")
            return {'error': str(e)}
    
    def _extract_visual_features(self, image: np.ndarray) -> Dict:
        """Extract visual features for uniqueness analysis"""
        try:
            # Convert to grayscale for texture analysis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Color features
            color_features = self._extract_color_features(image)
            
            # Texture features using Local Binary Pattern
            texture_features = self._extract_texture_features(gray)
            
            # Edge features
            edge_features = self._extract_edge_features(gray)
            
            # Shape features
            shape_features = self._extract_shape_features(gray)
            
            return {
                'color_features': color_features,
                'texture_features': texture_features,
                'edge_features': edge_features,
                'shape_features': shape_features
            }
            
        except Exception as e:
            logger.error(f"❌ Feature extraction failed: {e}")
            return {'error': str(e)}
    
    def _extract_color_features(self, image: np.ndarray) -> Dict:
        """Extract color-based features"""
        try:
            # Convert to different color spaces
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            
            # Calculate color histograms
            bgr_hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hsv_hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
            
            # Calculate color statistics
            color_stats = {
                'mean_bgr': np.mean(image, axis=(0, 1)).tolist(),
                'std_bgr': np.std(image, axis=(0, 1)).tolist(),
                'mean_hsv': np.mean(hsv, axis=(0, 1)).tolist(),
                'std_hsv': np.std(hsv, axis=(0, 1)).tolist(),
                'dominant_colors': self._find_dominant_colors(image, 5)
            }
            
            return color_stats
            
        except Exception as e:
            logger.error(f"❌ Color feature extraction failed: {e}")
            return {'error': str(e)}
    
    def _extract_texture_features(self, gray: np.ndarray) -> Dict:
        """Extract texture features using LBP and GLCM"""
        try:
            # Local Binary Pattern
            lbp = local_binary_pattern(gray, self.lbp_n_points, self.lbp_radius, method='uniform')
            lbp_hist, _ = np.histogram(lbp, bins=10, range=(0, 10), density=True)
            
            # Gray Level Co-occurrence Matrix
            glcm = graycomatrix(gray, self.glcm_distances, self.glcm_angles, 256, symmetric=True, normed=True)
            
            # GLCM properties
            contrast = graycoprops(glcm, 'contrast').flatten()
            dissimilarity = graycoprops(glcm, 'dissimilarity').flatten()
            homogeneity = graycoprops(glcm, 'homogeneity').flatten()
            energy = graycoprops(glcm, 'energy').flatten()
            correlation = graycoprops(glcm, 'correlation').flatten()
            
            return {
                'lbp_histogram': lbp_hist.tolist(),
                'glcm_contrast': contrast.tolist(),
                'glcm_dissimilarity': dissimilarity.tolist(),
                'glcm_homogeneity': homogeneity.tolist(),
                'glcm_energy': energy.tolist(),
                'glcm_correlation': correlation.tolist()
            }
            
        except Exception as e:
            logger.error(f"❌ Texture feature extraction failed: {e}")
            return {'error': str(e)}
    
    def _extract_edge_features(self, gray: np.ndarray) -> Dict:
        """Extract edge-based features"""
        try:
            # Canny edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Sobel gradients
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            
            # Edge statistics
            edge_density = np.sum(edges > 0) / edges.size
            gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
            gradient_direction = np.arctan2(sobely, sobelx)
            
            return {
                'edge_density': float(edge_density),
                'gradient_magnitude_mean': float(np.mean(gradient_magnitude)),
                'gradient_magnitude_std': float(np.std(gradient_magnitude)),
                'gradient_direction_mean': float(np.mean(gradient_direction)),
                'gradient_direction_std': float(np.std(gradient_direction))
            }
            
        except Exception as e:
            logger.error(f"❌ Edge feature extraction failed: {e}")
            return {'error': str(e)}
    
    def _extract_shape_features(self, gray: np.ndarray) -> Dict:
        """Extract shape-based features"""
        try:
            # Find contours
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return {'error': 'No contours found'}
            
            # Analyze largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            # Calculate shape metrics
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
            else:
                circularity = 0
            
            # Bounding rectangle
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = w / h if h > 0 else 0
            
            return {
                'contour_area': float(area),
                'contour_perimeter': float(perimeter),
                'circularity': float(circularity),
                'aspect_ratio': float(aspect_ratio),
                'bounding_box': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
            }
            
        except Exception as e:
            logger.error(f"❌ Shape feature extraction failed: {e}")
            return {'error': str(e)}
    
    def _find_dominant_colors(self, image: np.ndarray, n_colors: int = 5) -> List[List[int]]:
        """Find dominant colors in the image"""
        try:
            # Reshape image to 2D array of pixels
            pixels = image.reshape(-1, 3)
            
            # Use k-means to find dominant colors
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Get colors and their counts
            colors = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            
            # Count occurrences
            counts = np.bincount(labels)
            
            # Sort by count (most frequent first)
            sorted_indices = np.argsort(counts)[::-1]
            dominant_colors = colors[sorted_indices].tolist()
            
            return dominant_colors
            
        except Exception as e:
            logger.error(f"❌ Dominant color extraction failed: {e}")
            return []
    
    def _generate_uniqueness_signature(self, image: np.ndarray) -> str:
        """Generate a unique signature for the image based on its features"""
        try:
            # Create a feature vector
            features = []
            
            # Add color features
            features.extend(np.mean(image, axis=(0, 1)))
            features.extend(np.std(image, axis=(0, 1)))
            
            # Add texture features (simplified)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            lbp = local_binary_pattern(gray, 8, 1, method='uniform')
            lbp_hist, _ = np.histogram(lbp, bins=10, range=(0, 10), density=True)
            features.extend(lbp_hist)
            
            # Add edge density
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            features.append(edge_density)
            
            # Convert to string and hash
            feature_string = ','.join([str(f) for f in features])
            signature = hashlib.md5(feature_string.encode()).hexdigest()
            
            return signature
            
        except Exception as e:
            logger.error(f"❌ Uniqueness signature generation failed: {e}")
            return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()
    
    def compare_uniforms(self, annotation1: Dict, annotation2: Dict) -> Dict:
        """
        Compare two uniform annotations for similarity
        
        Args:
            annotation1: First uniform annotation
            annotation2: Second uniform annotation
            
        Returns:
            Dictionary containing similarity metrics
        """
        try:
            # Extract features for comparison
            features1 = annotation1.get('visual_features', {})
            features2 = annotation2.get('visual_features', {})
            
            if 'error' in features1 or 'error' in features2:
                return {'error': 'One or both annotations have errors'}
            
            # Calculate similarity scores
            color_similarity = self._compare_color_features(
                features1.get('color_features', {}),
                features2.get('color_features', {})
            )
            
            texture_similarity = self._compare_texture_features(
                features1.get('texture_features', {}),
                features2.get('texture_features', {})
            )
            
            edge_similarity = self._compare_edge_features(
                features1.get('edge_features', {}),
                features2.get('edge_features', {})
            )
            
            # Overall similarity (weighted average)
            weights = {'color': 0.4, 'texture': 0.4, 'edge': 0.2}
            overall_similarity = (
                color_similarity * weights['color'] +
                texture_similarity * weights['texture'] +
                edge_similarity * weights['edge']
            )
            
            return {
                'overall_similarity': float(overall_similarity),
                'color_similarity': float(color_similarity),
                'texture_similarity': float(texture_similarity),
                'edge_similarity': float(edge_similarity),
                'is_similar': overall_similarity > 0.7,  # Threshold for similarity
                'similarity_threshold': 0.7
            }
            
        except Exception as e:
            logger.error(f"❌ Uniform comparison failed: {e}")
            return {'error': str(e)}
    
    def _compare_color_features(self, color1: Dict, color2: Dict) -> float:
        """Compare color features between two uniforms"""
        try:
            if 'error' in color1 or 'error' in color2:
                return 0.0
            
            # Compare mean colors
            mean1 = np.array(color1.get('mean_bgr', [0, 0, 0]))
            mean2 = np.array(color2.get('mean_bgr', [0, 0, 0]))
            
            # Euclidean distance between color means
            color_distance = np.linalg.norm(mean1 - mean2)
            max_distance = np.sqrt(255**2 * 3)  # Maximum possible distance
            
            # Convert to similarity (0 = identical, 1 = completely different)
            color_similarity = 1 - (color_distance / max_distance)
            
            return max(0.0, min(1.0, color_similarity))
            
        except Exception as e:
            logger.error(f"❌ Color comparison failed: {e}")
            return 0.0
    
    def _compare_texture_features(self, texture1: Dict, texture2: Dict) -> float:
        """Compare texture features between two uniforms"""
        try:
            if 'error' in texture1 or 'error' in texture2:
                return 0.0
            
            # Compare LBP histograms
            lbp1 = np.array(texture1.get('lbp_histogram', []))
            lbp2 = np.array(texture2.get('lbp_histogram', []))
            
            if len(lbp1) == 0 or len(lbp2) == 0:
                return 0.0
            
            # Cosine similarity between histograms
            dot_product = np.dot(lbp1, lbp2)
            norm1 = np.linalg.norm(lbp1)
            norm2 = np.linalg.norm(lbp2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            texture_similarity = dot_product / (norm1 * norm2)
            
            return max(0.0, min(1.0, texture_similarity))
            
        except Exception as e:
            logger.error(f"❌ Texture comparison failed: {e}")
            return 0.0
    
    def _compare_edge_features(self, edge1: Dict, edge2: Dict) -> float:
        """Compare edge features between two uniforms"""
        try:
            if 'error' in edge1 or 'error' in edge2:
                return 0.0
            
            # Compare edge density
            density1 = edge1.get('edge_density', 0)
            density2 = edge2.get('edge_density', 0)
            
            if density1 == 0 and density2 == 0:
                return 1.0  # Both have no edges
            
            # Calculate similarity based on edge density difference
            density_diff = abs(density1 - density2)
            max_density = max(density1, density2)
            
            if max_density == 0:
                return 1.0
            
            edge_similarity = 1 - (density_diff / max_density)
            
            return max(0.0, min(1.0, edge_similarity))
            
        except Exception as e:
            logger.error(f"❌ Edge comparison failed: {e}")
            return 0.0
    
    def create_annotated_image(self, image_path: str, annotation_data: Dict, 
                              output_path: str = None) -> str:
        """
        Create an annotated version of the image with detection boxes and labels
        
        Args:
            image_path: Path to original image
            annotation_data: Annotation data from annotate_uniform
            output_path: Path for output image (optional)
            
        Returns:
            Path to the annotated image
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert to PIL for better text rendering
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            draw = ImageDraw.Draw(pil_image)
            
            # Try to load a font, fall back to default if not available
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Draw detection boxes
            detections = annotation_data.get('detection_results', {}).get('detections', [])
            for detection in detections:
                bbox = detection.get('bbox', {})
                class_name = detection.get('class_name', 'Unknown')
                confidence = detection.get('confidence', 0)
                
                # Draw bounding box
                x1, y1, x2, y2 = int(bbox['x1']), int(bbox['y1']), int(bbox['x2']), int(bbox['y2'])
                draw.rectangle([x1, y1, x2, y2], outline='red', width=3)
                
                # Draw label
                label = f"{class_name}: {confidence:.2f}"
                draw.text((x1, y1-20), label, fill='red', font=font)
            
            # Draw logo annotations
            logo_candidates = annotation_data.get('logo_analysis', {}).get('logo_candidates', [])
            for logo in logo_candidates:
                bbox = logo.get('bbox', {})
                x, y, w, h = bbox.get('x', 0), bbox.get('y', 0), bbox.get('width', 0), bbox.get('height', 0)
                
                # Draw logo box in green
                draw.rectangle([x, y, x + w, y + h], outline='green', width=2)
                
                # Draw logo label
                distinctiveness = logo.get('distinctiveness', 0)
                label = f"Logo: {distinctiveness:.2f}"
                draw.text((x, y-15), label, fill='green', font=font)
            
            # Draw text/insignia annotations
            text_candidates = annotation_data.get('text_analysis', {}).get('text_candidates', [])
            for text_region in text_candidates:
                bbox = text_region.get('bbox', {})
                x, y, w, h = bbox.get('x', 0), bbox.get('y', 0), bbox.get('width', 0), bbox.get('height', 0)
                
                # Draw text region box in blue
                draw.rectangle([x, y, x + w, y + h], outline='blue', width=2)
                
                # Draw text label
                label = "Text/Insignia"
                draw.text((x, y-15), label, fill='blue', font=font)
            
            # Add comprehensive annotation info
            info_text = [
                f"UNIFORM ANALYSIS REPORT",
                f"Timestamp: {annotation_data.get('annotation_timestamp', 'Unknown')}",
                f"Detections: {len(detections)}",
                f"Logos Found: {len(logo_candidates)}",
                f"Text Regions: {len(text_candidates)}",
                f"Primary Colors: {len(annotation_data.get('color_analysis', {}).get('primary_colors', []))}",
                f"Color Temp: {annotation_data.get('color_analysis', {}).get('color_harmony', {}).get('color_temperature', 'Unknown')}",
                f"Fabric Texture: {annotation_data.get('uniform_features', {}).get('fabric_smoothness', 0):.3f}",
                f"Signature: {annotation_data.get('uniqueness_signature', 'Unknown')[:8]}..."
            ]
            
            y_offset = 30
            for text in info_text:
                # Add background for better readability
                bbox = draw.textbbox((10, y_offset), text, font=font)
                draw.rectangle(bbox, fill='white', outline='black', width=1)
                draw.text((10, y_offset), text, fill='black', font=font)
                y_offset += 25
            
            # Save annotated image
            if output_path is None:
                base_name = os.path.splitext(image_path)[0]
                output_path = f"{base_name}_annotated.jpg"
            
            pil_image.save(output_path, "JPEG", quality=95)
            logger.info(f"✅ Annotated image saved to: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Failed to create annotated image: {e}")
            return image_path  # Return original path if annotation fails

# Utility functions for batch processing
def batch_annotate_uniforms(image_paths: List[str], output_dir: str = None) -> List[Dict]:
    """
    Batch annotate multiple uniform images
    
    Args:
        image_paths: List of image paths to annotate
        output_dir: Directory to save annotated images (optional)
        
    Returns:
        List of annotation results
    """
    annotator = UniformAnnotator()
    results = []
    
    for image_path in image_paths:
        try:
            # Annotate uniform
            annotation = annotator.annotate_uniform(image_path)
            
            # Create annotated image if output directory specified
            if output_dir and not annotation.get('error'):
                os.makedirs(output_dir, exist_ok=True)
                annotated_path = annotator.create_annotated_image(
                    image_path, annotation, 
                    os.path.join(output_dir, f"annotated_{os.path.basename(image_path)}")
                )
                annotation['annotated_image_path'] = annotated_path
            
            results.append(annotation)
            
        except Exception as e:
            logger.error(f"❌ Failed to annotate {image_path}: {e}")
            results.append({
                'error': str(e),
                'image_path': image_path
            })
    
    return results

def find_similar_uniforms(target_annotation: Dict, all_annotations: List[Dict], 
                         similarity_threshold: float = 0.7) -> List[Dict]:
    """
    Find uniforms similar to a target uniform
    
    Args:
        target_annotation: Annotation of the target uniform
        all_annotations: List of all uniform annotations to compare against
        similarity_threshold: Minimum similarity score (0.0 to 1.0)
        
    Returns:
        List of similar uniforms with similarity scores
    """
    annotator = UniformAnnotator()
    similar_uniforms = []
    
    for annotation in all_annotations:
        if annotation.get('error') or annotation == target_annotation:
            continue
        
        try:
            similarity = annotator.compare_uniforms(target_annotation, annotation)
            
            if not similarity.get('error') and similarity.get('overall_similarity', 0) >= similarity_threshold:
                similar_uniforms.append({
                    'annotation': annotation,
                    'similarity_score': similarity.get('overall_similarity', 0),
                    'similarity_details': similarity
                })
        
        except Exception as e:
            logger.error(f"❌ Failed to compare uniforms: {e}")
            continue
    
    # Sort by similarity score (highest first)
    similar_uniforms.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    return similar_uniforms
