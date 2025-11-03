"""
Ayurvedic Knowledge Base
This module provides structured Ayurvedic knowledge for the vector database.
"""

def get_ayurveda_documents():
    """Return list of Ayurvedic knowledge documents with metadata"""
    
    documents = []
    
    # Fundamental Concepts
    documents.extend([
        {
            'text': "Agni is the digestive fire central to Ayurvedic health. Jatharagni, located in the stomach and small intestine, transforms food into nutrients and energy. When Agni is balanced (Sama Agni), digestion is optimal. Weak Agni (Manda Agni) causes accumulation of Ama (toxins), while excessive Agni (Tikshna Agni) burns nutrients too quickly.",
            'metadata': {'category': 'concepts', 'topic': 'agni'}
        },
        {
            'text': "Ama is undigested food material that becomes toxic. It is sticky, heavy, and clogs the body's channels (srotas). Ama accumulation is the root cause of most diseases. Signs include thick coating on tongue, lethargy, body aches, and sluggish digestion.",
            'metadata': {'category': 'concepts', 'topic': 'ama'}
        },
        {
            'text': "The liver (Yakrit) in Ayurveda governs transformation and filtration. It produces Pitta and regulates blood sugar through the transformation of Rasa dhatu. A healthy liver maintains balanced Agni and prevents Ama formation.",
            'metadata': {'category': 'organs', 'topic': 'liver'}
        },
        {
            'text': "The pancreas governs insulin production and blood sugar regulation. In Ayurveda, this relates to the function of Jatharagni and the metabolism of sweet taste (Madhura rasa). Weakness here leads to Prameha (urinary disorders including diabetes).",
            'metadata': {'category': 'organs', 'topic': 'pancreas'}
        }
    ])
    
    # Vata Dosha Guidelines
    documents.extend([
        {
            'text': "Vata dosha dietary guidelines: Favor warm, moist, oily, grounding foods. Include cooked root vegetables like carrots, beets, sweet potatoes. Use warming spices: ginger, cinnamon, cardamom, cumin. Prefer sweet fruits like bananas, dates, and soaked raisins. Use ghee and sesame oil liberally.",
            'metadata': {'category': 'diet', 'dosha': 'vata', 'topic': 'favor'}
        },
        {
            'text': "Vata dosha foods to avoid: Reduce cold, dry, light foods. Minimize raw vegetables, especially cabbage, broccoli, cauliflower. Avoid dried fruits, crackers, and chips. Limit beans except mung dal and red lentils when well-cooked with spices. Avoid ice-cold drinks and carbonated beverages.",
            'metadata': {'category': 'diet', 'dosha': 'vata', 'topic': 'avoid'}
        },
        {
            'text': "Vata metabolism tends to be irregular (Vishama Agni). This causes variable appetite, gas, bloating, constipation. To balance: eat regular meals, favor warm cooked foods, use digestive spices, practice gentle exercise like walking or yoga.",
            'metadata': {'category': 'metabolism', 'dosha': 'vata'}
        }
    ])
    
    # Pitta Dosha Guidelines
    documents.extend([
        {
            'text': "Pitta dosha dietary guidelines: Favor cool, refreshing, slightly dry foods. Include sweet fruits like melons, grapes, cherries, pears. Use bitter greens like kale, collards, dandelion. Favor cooling spices: fennel, coriander, cilantro, mint. Use ghee moderately. Include basmati rice, barley, oats.",
            'metadata': {'category': 'diet', 'dosha': 'pitta', 'topic': 'favor'}
        },
        {
            'text': "Pitta dosha foods to avoid: Reduce hot, spicy, oily, fried foods. Minimize sour tastes like vinegar, pickles, fermented foods. Avoid pungent vegetables: onions, garlic, radishes, hot peppers. Limit sour fruits and citrus. Avoid or minimize alcohol, caffeine, and red meat.",
            'metadata': {'category': 'diet', 'dosha': 'pitta', 'topic': 'avoid'}
        },
        {
            'text': "Pitta metabolism is sharp and intense (Tikshna Agni). This creates strong hunger, tendency to acidity, and rapid digestion. To balance: eat cooling foods, avoid skipping meals, favor bitter and sweet tastes, practice calming activities.",
            'metadata': {'category': 'metabolism', 'dosha': 'pitta'}
        }
    ])
    
    # Kapha Dosha Guidelines
    documents.extend([
        {
            'text': "Kapha dosha dietary guidelines: Favor light, warm, dry, pungent foods. Include all spices especially ginger, black pepper, turmeric, cayenne. Use bitter and astringent tastes: leafy greens, cruciferous vegetables, legumes. Favor light fruits like apples, pears, pomegranates. Use minimal oil.",
            'metadata': {'category': 'diet', 'dosha': 'kapha', 'topic': 'favor'}
        },
        {
            'text': "Kapha dosha foods to avoid: Reduce heavy, oily, cold, sweet foods. Minimize dairy products especially cheese, yogurt, ice cream. Avoid sweet heavy fruits like bananas, avocados, coconuts. Limit wheat, rice, and other heavy grains. Reduce fried foods and excess fats.",
            'metadata': {'category': 'diet', 'dosha': 'kapha', 'topic': 'avoid'}
        },
        {
            'text': "Kapha metabolism is slow and heavy (Manda Agni). This causes slow digestion, weight gain, lethargy, excess mucus. To balance: eat light spicy foods, skip breakfast or have light breakfast, use digestive spices, practice vigorous exercise.",
            'metadata': {'category': 'metabolism', 'dosha': 'kapha'}
        }
    ])
    
    # Blood Glucose Management
    documents.extend([
        {
            'text': "For blood glucose management favor: bitter gourd (karela), fenugreek seeds, cinnamon, turmeric, amla (Indian gooseberry), gymnema sylvestre, neem leaves, bitter leafy greens. These enhance insulin sensitivity and glucose metabolism.",
            'metadata': {'category': 'conditions', 'topic': 'glucose'}
        },
        {
            'text': "Blood glucose regulation through diet: Emphasize complex carbohydrates like barley, millet, quinoa. Include plenty of fiber from vegetables and legumes. Use cinnamon, fenugreek, and bitter melon. Avoid simple sugars, white rice, and refined flours. Eat smaller frequent meals.",
            'metadata': {'category': 'conditions', 'topic': 'glucose'}
        },
        {
            'text': "Ayurvedic approach to diabetes (Prameha): Results from impaired Agni and accumulation of Ama. Treatment includes strengthening digestion, using bitter herbs, reducing Kapha, regular exercise, and stress management. Key herbs: bitter melon, fenugreek, turmeric, gudmar.",
            'metadata': {'category': 'conditions', 'topic': 'diabetes'}
        }
    ])
    
    # Cholesterol Management
    documents.extend([
        {
            'text': "For cholesterol management favor: garlic, turmeric, guggul, arjuna, coriander seeds, ginger, fenugreek, oats, barley. These herbs and foods support healthy lipid metabolism and liver function.",
            'metadata': {'category': 'conditions', 'topic': 'cholesterol'}
        },
        {
            'text': "Cholesterol reduction diet: Increase fiber-rich foods like oats, barley, vegetables. Use heart-healthy fats like ghee in moderation and cold-pressed oils. Include garlic, turmeric, and coriander. Avoid fried foods, excess dairy, and heavy red meats.",
            'metadata': {'category': 'conditions', 'topic': 'cholesterol'}
        }
    ])
    
    # Liver Health
    documents.extend([
        {
            'text': "Liver health (Yakrit) support: Favor bitter tastes - bitter gourd, neem, turmeric, dandelion, milk thistle. Include cooling foods to balance Pitta which governs liver. Use aloe vera juice, amla, and bhumi amla. Practice intermittent fasting.",
            'metadata': {'category': 'organs', 'topic': 'liver'}
        },
        {
            'text': "Liver detoxification foods: Turmeric, milk thistle, dandelion root, beets, carrots, leafy greens, lemon, apple cider vinegar. These support liver's natural detox processes and help clear Ama.",
            'metadata': {'category': 'organs', 'topic': 'liver'}
        }
    ])
    
    # Digestive Health
    documents.extend([
        {
            'text': "To strengthen Agni: Use warming spices - ginger, black pepper, cumin, coriander, fennel. Drink warm water or ginger tea. Avoid cold drinks with meals. Eat in a calm environment. Don't overeat. Wait 3-6 hours between meals.",
            'metadata': {'category': 'digestion', 'topic': 'agni'}
        },
        {
            'text': "Digestive spice blend (CCF tea): Equal parts cumin, coriander, fennel seeds. Boil 1 tsp in water, strain and sip. This balances all three doshas, kindles Agni, and reduces gas and bloating.",
            'metadata': {'category': 'digestion', 'topic': 'remedies'}
        },
        {
            'text': "Food combining rules: Don't mix milk with sour fruits or meat. Don't heat honey above 108°F. Eat fruits alone or before meals. Don't mix very hot and very cold foods. Avoid yogurt at night.",
            'metadata': {'category': 'digestion', 'topic': 'food-combining'}
        }
    ])
    
    # Specific Foods
    documents.extend([
        {
            'text': "Bitter melon (karela): Powerful blood glucose regulator. Contains compounds that mimic insulin. Best consumed as juice (2-3 oz) in morning on empty stomach or cooked as vegetable. Quantity: 50-100g daily for diabetes management.",
            'metadata': {'category': 'foods', 'topic': 'bitter-melon'}
        },
        {
            'text': "Fenugreek seeds (methi): Lowers blood sugar and cholesterol. Soak 1 tsp seeds overnight, consume with water in morning. Or use as spice in cooking. Quantity: 2-5g powder twice daily for glucose control.",
            'metadata': {'category': 'foods', 'topic': 'fenugreek'}
        },
        {
            'text': "Turmeric (haldi): Anti-inflammatory, supports liver, improves insulin sensitivity. Use 1/2 to 1 tsp daily in cooking or golden milk. Combine with black pepper for absorption. Safe up to 3g daily.",
            'metadata': {'category': 'foods', 'topic': 'turmeric'}
        },
        {
            'text': "Cinnamon (dalchini): Enhances insulin sensitivity and glucose metabolism. Add 1/2 tsp to food or tea daily. Quantity: 1-6g daily is safe and effective for blood sugar management.",
            'metadata': {'category': 'foods', 'topic': 'cinnamon'}
        },
        {
            'text': "Amla (Indian gooseberry): Rich in vitamin C, supports pancreas and liver function, balances blood sugar. Take 1-2 fresh amla daily or 1 tsp powder with water. Excellent for Pitta balance.",
            'metadata': {'category': 'foods', 'topic': 'amla'}
        },
        {
            'text': "Barley (yava): Light grain that kindles Agni without raising blood sugar significantly. Good for Kapha types and diabetes. Use 50-100g daily as porridge or in soups.",
            'metadata': {'category': 'foods', 'topic': 'barley'}
        },
        {
            'text': "Mung dal: Most balanced legume, tridoshic. Easy to digest, doesn't create Ama. Good protein source for diabetes management. Cook 1/2 cup daily with cumin, coriander, turmeric.",
            'metadata': {'category': 'foods', 'topic': 'mung-dal'}
        },
        {
            'text': "Leafy greens (kale, spinach, collards): Bitter taste supports liver, reduces Kapha, provides minerals. Include 1-2 cups daily cooked. Especially good for Pitta and Kapha types.",
            'metadata': {'category': 'foods', 'topic': 'greens'}
        }
    ])
    
    # Meal Timing and Structure
    documents.extend([
        {
            'text': "Ideal meal timing: Breakfast (7-8am) light, Lunch (12-1pm) largest meal when Agni is strongest, Dinner (6-7pm) light and early. Avoid eating after 8pm. Wait 3-4 hours between meals.",
            'metadata': {'category': 'lifestyle', 'topic': 'meal-timing'}
        },
        {
            'text': "Meal structure: Start with sweet taste (grains), then sour and salty (vegetables with spices), end with pungent, bitter, astringent (leafy greens, lentils). This supports natural digestive sequence.",
            'metadata': {'category': 'lifestyle', 'topic': 'meal-structure'}
        }
    ])
    
    # Exercise
    documents.extend([
        {
            'text': "Exercise for Vata: Gentle, grounding activities. Walking, gentle yoga, tai chi, swimming. 20-30 minutes daily. Avoid excessive or intense exercise which aggravates Vata.",
            'metadata': {'category': 'lifestyle', 'dosha': 'vata', 'topic': 'exercise'}
        },
        {
            'text': "Exercise for Pitta: Moderate intensity, cooling activities. Swimming, walking in nature, moon-lit walks, gentle to moderate yoga. 30-45 minutes daily. Avoid competition and overheating.",
            'metadata': {'category': 'lifestyle', 'dosha': 'pitta', 'topic': 'exercise'}
        },
        {
            'text': "Exercise for Kapha: Vigorous, stimulating activities. Running, aerobics, hot yoga, weight training. 45-60 minutes daily. Kapha benefits most from intense exercise.",
            'metadata': {'category': 'lifestyle', 'dosha': 'kapha', 'topic': 'exercise'}
        }
    ])
    
    return documents


def get_food_database():
    """Return detailed food database with Ayurvedic properties"""
    
    return [
        {
            'name': 'Bitter Melon',
            'sanskrit': 'Karela',
            'taste': 'Bitter',
            'qualities': 'Light, dry',
            'effect_on_doshas': 'Reduces Kapha and Pitta, increases Vata',
            'benefits': 'Lowers blood glucose, supports pancreas, cleanses liver, reduces cholesterol',
            'quantity': '50-100g daily or 2-3 oz juice',
            'preparation': 'Cook as vegetable or juice on empty stomach',
            'conditions': ['diabetes', 'high cholesterol', 'liver support']
        },
        {
            'name': 'Fenugreek Seeds',
            'sanskrit': 'Methi',
            'taste': 'Bitter, pungent',
            'qualities': 'Hot, unctuous',
            'effect_on_doshas': 'Balances Vata and Kapha, may increase Pitta',
            'benefits': 'Lowers blood sugar and cholesterol, improves digestion, galactagogue',
            'quantity': '2-5g powder twice daily',
            'preparation': 'Soak overnight and eat seeds, or use powder in cooking',
            'conditions': ['diabetes', 'high cholesterol', 'digestive weakness']
        },
        {
            'name': 'Turmeric',
            'sanskrit': 'Haldi',
            'taste': 'Bitter, pungent',
            'qualities': 'Hot, dry, light',
            'effect_on_doshas': 'Balances all doshas, especially Kapha',
            'benefits': 'Anti-inflammatory, supports liver, improves insulin sensitivity, blood purifier',
            'quantity': '1-3g daily',
            'preparation': 'Use in cooking, golden milk, or with honey. Combine with black pepper',
            'conditions': ['diabetes', 'inflammation', 'liver support', 'high cholesterol']
        }
    ]