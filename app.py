import streamlit as st

nouns = {
    "cyning": {"translation": "king", "case": "nominative", "semantic_role": "АГЕНС"},
    "cyninge": {"translation": "king", "case": "dative", "semantic_role": "РЕЦИПИЕНТ"},
    "þegn": {"translation": "thane", "case": "nominative", "semantic_role": "АГЕНС"},
    "þegne": {"translation": "thane", "case": "dative", "semantic_role": "РЕЦИПИЕНТ"},
    "hlāford": {"translation": "lord", "case": "nominative", "semantic_role": "АГЕНС"},
    "hlāforde": {"translation": "lord", "case": "dative", "semantic_role": "РЕЦИПИЕНТ"},
    "freond": {"translation": "friend", "case": "nominative", "semantic_role": "АГЕНС"},
    "freonde": {"translation": "friend", "case": "dative", "semantic_role": "РЕЦИПИЕНТ"},
    "freondes": {"translation": "friend", "case": "genitive", "semantic_role": "АГЕНС"},
    "he": {"translation": "he", "case": "nominative", "semantic_role": "АГЕНС"},
    "hē": {"translation": "he", "case": "nominative", "semantic_role": "АГЕНС"},
    "his": {"translation": "his", "case": "genitive", "semantic_role": "АГЕНС"},
    "cnapan": {"translation": "boy", "case": "genitive", "semantic_role": "АГЕНС"},
    "þæs": {"translation": "the", "case": "genitive", "semantic_role": None},
    "sēo": {"translation": "she", "case": "nominative", "semantic_role": "АГЕНС"},
    "cwēn": {"translation": "queen", "case": "nominative", "semantic_role": "АГЕНС"},
    "cwēne": {"translation": "queen", "case": "dative", "semantic_role": "РЕЦИПИЕНТ"},
    "hire": {"translation": "her", "case": "genitive", "semantic_role": "АГЕНС"},
    "þegnes": {"translation": "thane's", "case": "genitive", "semantic_role": "АГЕНС"}
}

verbs = {
    "helpan": {"translation": "help", "expected_obj_case": "dative", "requires_preposition": False, "preposition": None, "semantic": {"role_subj": "АГЕНС", "role_obj": "РЕЦИПИЕНТ", "relation": "ВОЗДЕЙСТВИЕ"}},
    "lōcian": {"translation": "look", "expected_obj_case": "genitive", "requires_preposition": True, "preposition": "at", "semantic": {"role_subj": "ЭКСПЕРИЕНЦЕР", "role_obj": "ИСТОЧНИК", "relation": "ВОСПРИЯТИЕ"}},
    "lōcode": {"translation": "look", "expected_obj_case": "genitive", "requires_preposition": True, "preposition": "at", "semantic": {"role_subj": "ЭКСПЕРИЕНЦЕР", "role_obj": "ИСТОЧНИК", "relation": "ВОСПРИЯТИЕ"}},
    "bīdan": {"translation": "wait", "expected_obj_case": "genitive", "requires_preposition": True, "preposition": "for", "semantic": {"role_subj": "ЭКСПЕРИЕНЦЕР", "role_obj": "ЦЕЛЬ", "relation": "НАПРАВЛЕННОСТЬ"}},
    "bād": {"translation": "wait", "expected_obj_case": "genitive", "requires_preposition": True, "preposition": "for", "semantic": {"role_subj": "ЭКСПЕРИЕНЦЕР", "role_obj": "ЦЕЛЬ", "relation": "НАПРАВЛЕННОСТЬ"}},
    "andswarian": {"translation": "answer", "expected_obj_case": "dative", "requires_preposition": False, "preposition": None, "semantic": {"role_subj": "АГЕНС", "role_obj": "РЕЦИПИЕНТ", "relation": "ДЕЙСТВИЕ"}},
    "andswarode": {"translation": "answer", "expected_obj_case": "dative", "requires_preposition": False, "preposition": None, "semantic": {"role_subj": "АГЕНС", "role_obj": "РЕЦИПИЕНТ", "relation": "ДЕЙСТВИЕ"}}
}

def tokenize(sentence):
    punctuation = ['.', ',', ';', ':', '?', '!', '(', ')', '"', "'"]
    for p in punctuation:
        sentence = sentence.replace(p, ' ')
    return sentence.lower().split()

def find_verb(tokens, verbs_dict):
    for token in tokens:
        if token in verbs_dict:
            return token, verbs_dict[token]
    return None, None

def get_case(word, nouns_dict):
    if word is None:
        return None
    word_lower = word.lower()
    if word_lower in nouns_dict:
        return nouns_dict[word_lower].get('case')
    return None

def translate_word(word, nouns_dict):
    if word is None:
        return None
    word_lower = word.lower()
    if word_lower in nouns_dict:
        return nouns_dict[word_lower].get('translation')
    return word

def extract_arguments(tokens, verb_index, expected_obj_case, nouns_dict):
    subj = None
    obj = None
    
    for i in range(verb_index - 1, -1, -1):
        if get_case(tokens[i], nouns_dict) == 'nominative':
            subj = tokens[i]
            break
    
    for i in range(verb_index + 1, len(tokens)):
        token = tokens[i]
        case = get_case(token, nouns_dict)
        translation = nouns_dict.get(token, {}).get('translation', '')
        
        if translation in ['the', 'his', 'her']:
            continue
        
        if case == expected_obj_case:
            obj = token
            break
    
    return subj, obj

def generate_pde(verb_info, subj, obj, tokens, nouns_dict):
    pde_verb = verb_info['translation']
    if subj:
        s = translate_word(subj, nouns_dict)
        if s and s not in ['me', 'he', 'she', 'it', 'we', 'they', 'you'] and not s.startswith('the '):
            s = f"the {s}"
    else:
        s = "[subject not found]"
    if obj:
        o = translate_word(obj, nouns_dict)
        if o and o not in ['me', 'he', 'she', 'it', 'we', 'they', 'you'] and not o.startswith('the '):
            o = o
    else:
        o = "[object not found]"
    pos = "his " if 'his' in tokens else ""
    if verb_info.get('requires_preposition'):
        return f"{s.capitalize()} {pde_verb}s {verb_info['preposition']} {pos}{o}"
    return f"{s.capitalize()} {pde_verb}s {pos}{o}"

def get_semantic_role(word, nouns_dict):
    if word is None:
        return None
    word_lower = word.lower()
    if word_lower in nouns_dict:
        return nouns_dict[word_lower].get('semantic_role')
    return None

def generate_constructive_model(verb_info, subj, obj, nouns_dict, period='oe'):
    if not verb_info or not subj or not obj:
        return "недостаточно данных"
    sem = verb_info.get('semantic', {})
    r_subj = get_semantic_role(subj, nouns_dict) or sem.get('role_subj', 'УЧАСТНИК')
    r_obj = get_semantic_role(obj, nouns_dict) or sem.get('role_obj', 'УЧАСТНИК')
    rel = sem.get('relation', 'ДЕЙСТВИЕ')
    cmap = {'nominative': 'им', 'dative': 'дат', 'genitive': 'род', 'accusative': 'вин'}
    if period == 'oe':
        cs = cmap.get(get_case(subj, nouns_dict) or 'им', 'им')
        co = cmap.get(verb_info.get('expected_obj_case', '?'), '?')
        sw, ow = subj, obj
    else:
        cs = 'им'
        co = verb_info.get('preposition', 'вин') if verb_info.get('requires_preposition') else 'вин'
        sw = translate_word(subj, nouns_dict) or subj
        ow = translate_word(obj, nouns_dict) or obj
        if sw and sw not in ['he', 'she', 'it', 'we', 'they', 'you', 'i', 'me']:
            sw = f"the {sw}"
    return f"{r_subj}[{cs}] ({sw}) - {rel} - {r_obj}[{co}] ({ow})"

def analyze(oe_sentence, show_constructive, show_subcat):
    if not oe_sentence or not oe_sentence.strip():
        return "Введите предложение"
    tokens = tokenize(oe_sentence)
    verb, vinfo = find_verb(tokens, verbs)
    if not verb:
        return f"Глагол не найден\n\nТокены: {tokens}"
    vi = tokens.index(verb)
    exp_case = vinfo.get('expected_obj_case', 'dative')
    subj, obj = extract_arguments(tokens, vi, exp_case, nouns)
    out = f"**Токены:** {tokens}\n\n"
    out += f"**Глагол:** {verb} → {vinfo['translation']}\n"
    
    if show_subcat:
        exp_case_str = exp_case if isinstance(exp_case, str) else ', '.join(exp_case)
        out += f"**SUBCAT-список:** `< NP[subj] (nom), NP[{exp_case_str}] >`\n\n"
    
    out += f"**Подлежащее:** {subj} ({get_case(subj, nouns)})\n"
    out += f"**Дополнение:** {obj} ({get_case(obj, nouns)})\n"
    if subj and obj:
        out += "\n**Валентность соблюдена**\n"
        out += f"**Перевод:** {generate_pde(vinfo, subj, obj, tokens, nouns)}"
    else:
        out += "\n**Валентность нарушена**"
    if show_constructive and subj and obj:
        out += f"\n\n**OE модель:** {generate_constructive_model(vinfo, subj, obj, nouns, 'oe')}"
        out += f"\n**PDE модель:** {generate_constructive_model(vinfo, subj, obj, nouns, 'pde')}"
    return out

st.set_page_config(page_title="OE Parser", page_icon="✑")
st.title("OE Parser — Лингвистический парсер древнеанглийского языка")
st.markdown("Анализирует валентность глаголов в древнеанглийских предложениях.")

if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

oe_input = st.text_area(
    "Древнеанглийское предложение (OE)", 
    value=st.session_state.input_text,
    height=100,
    placeholder="Например: Se cyning helpan his þegne"
)

col1, col2 = st.columns(2)
with col1:
    show_constructive = st.checkbox("Показать конструктивные модели", value=True)
with col2:
    show_subcat = st.checkbox("Показать SUBCAT-список", value=False)

if st.button("Анализировать", type="primary"):
    if oe_input:
        result = analyze(oe_input, show_constructive, show_subcat)
        st.markdown(result)
    else:
        st.warning("Введите предложение")

with st.expander("Примеры для тестирования"):
    examples = [
        "Se cyning helpan his þegne",
        "He lōcode þæs cnapan",
        "Hē bād his freondes",
        "Hē andswarode þām cyninge",
        "Se cyning lōcode his freondes",
        "Se hlāford helpan his freonde",
        "Sēo cwēn bād hire þegnes",
        "Se þegn andswarode sēo cwēne"
    ]
    for ex in examples:
        if st.button(ex):
            st.session_state.input_text = ex
            st.rerun()
