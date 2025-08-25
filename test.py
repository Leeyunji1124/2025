import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import os

# --- 함수 정의 (오류 수정을 위해 위로 이동) ---
def get_scientific_explanation(secret_var):
    explanations = {
        'light': "빛은 광합성에 필요한 에너지를 제공합니다. 빛의 세기가 증가하면 광합성 속도가 빨라져 식물 성장이 촉진되지만, 너무 강한 빛은 오히려 성장을 저해할 수 있습니다. 최적점은 5단계입니다.",
        'water': "물은 광합성 반응의 필수적인 재료입니다. 물이 충분해야 이산화탄소가 잎으로 흡수되고, 물 분해가 일어나 에너지를 얻을 수 있습니다. 물의 양이 5단계일 때 최적의 성장을 보입니다.",
        'co2': "이산화탄소는 광합성을 통해 포도당을 만드는 데 사용되는 주요 원료입니다. 이산화탄소 농도가 높을수록 광합성 속도가 빨라집니다. 5단계일 때 가장 효율적입니다."
    }
    return explanations.get(secret_var, "알 수 없는 변인입니다.")

def get_hint(secret_var):
    hints = {
        'light': "가로축이 '빛의 세기'인 그래프를 자세히 살펴보세요. 성장률이 어떤 패턴으로 변하는지 알 수 있을 거예요.",
        'water': "가로축이 '물의 양'인 그래프를 보면 다른 변인들과는 다른 뚜렷한 경향을 보일 거예요.",
        'co2': "이산화탄소 농도에 따른 성장률 변화가 가장 뚜렷하게 나타날 겁니다. 해당 그래프를 다시 확인해 보세요."
    }
    return hints.get(secret_var, "다시 실험을 진행하며 데이터를 더 모아보세요.")

# --- 페이지 설정 ---
st.set_page_config(
    page_title="광합성 탐정: 100% 성장 지점을 찾아라!",
    layout="wide"
)

st.title("🌱 광합성 탐정: 100% 성장 지점을 찾아라!")
st.write("여러분의 임무는 식물이 **가장 건강하게 자랄 수 있는 최적의 조건**을 찾아내는 것입니다. 실험을 반복하여 빛, 물, 이산화탄소 중 어떤 변인이 가장 큰 영향을 주는지, 그리고 그 변인의 **100% 성장 지점**은 몇인지 찾아보세요! (최적점은 1부터 10 사이의 정수입니다)")

# --- 세션 상태 초기화 ---
if 'secret_variable' not in st.session_state:
    st.session_state.secret_variable = random.choice(['light', 'water', 'co2'])
    st.session_state.experiment_log = pd.DataFrame(columns=['빛', '물', 'CO2', '성장률'])
    st.session_state.max_growth = random.uniform(50, 100) # 최대 성장률을 무작위로 설정
    st.session_state.optimal_value = 5 # 100% 성장 지점을 5로 변경

# --- UI 요소 ---
st.subheader("🧪 실험 조건 설정")
col1, col2, col3 = st.columns(3)

with col1:
    light_level = st.slider("☀️ 빛의 세기 (단계)", 1, 10, 5) # 슬라이더 범위 변경
with col2:
    water_level = st.slider("💧 물의 양 (단계)", 1, 10, 5) # 슬라이더 범위 변경
with col3:
    co2_level = st.slider("💨 이산화탄소 농도 (단계)", 1, 10, 5) # 슬라이더 범위 변경

# --- 실험 결과 계산 함수 ---
def calculate_growth(light, water, co2, secret_var, max_growth):
    growth_rate = 0
    # 성장률 계산식 변경 (최적점이 5가 되도록)
    if secret_var == 'light':
        growth_rate = -4 * (light - 5)**2 + 100
    elif secret_var == 'water':
        growth_rate = -4 * (water - 5)**2 + 100
    elif secret_var == 'co2':
        growth_rate = -4 * (co2 - 5)**2 + 100

    # 0보다 작거나 100보다 큰 값은 조정
    growth_rate = max(0, min(100, growth_rate))

    # 다른 변수들의 영향 (노이즈) 추가
    noise_factor = 2
    if secret_var != 'light':
        growth_rate -= noise_factor * abs(light - 5)
    if secret_var != 'water':
        growth_rate -= noise_factor * abs(water - 5)
    if secret_var != 'co2':
        growth_rate -= noise_factor * abs(co2 - 5)

    # 최종 성장률 계산
    final_growth = (growth_rate / 100) * max_growth
    final_growth = max(0, final_growth)
    return round(final_growth, 2)

# --- '실험 시작' 버튼 ---
if st.button("🔬 실험 시작"):
    current_growth = calculate_growth(light_level, water_level, co2_level, st.session_state.secret_variable, st.session_state.max_growth)
    new_row = pd.DataFrame([{'빛': light_level, '물': water_level, 'CO2': co2_level, '성장률': current_growth}])
    st.session_state.experiment_log = pd.concat([st.session_state.experiment_log, new_row], ignore_index=True)

    st.success(f"실험 완료! 이번 실험에서 식물은 **{current_growth}** 만큼 성장했습니다.")

    # --- 식물 성장 텍스트 표시 (이미지 대체 부분) ---
    st.subheader("🌱 식물 성장 모습")
    if current_growth < 25:
        st.write("🌱 아직 성장이 미미합니다.")
    elif current_growth < 50:
        st.write("🌿 조금씩 자라고 있네요!")
    elif current_growth < 75:
        st.write("🌳 제법 많이 자랐어요!")
    else:
        st.write("🌲 매우 건강하게 잘 자랐습니다!")

# --- 실험 기록 및 시각화 ---
if not st.session_state.experiment_log.empty:
    st.subheader("📚 실험 기록")
    st.dataframe(st.session_state.experiment_log, use_container_width=True)

    st.subheader("📈 성장률 그래프")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(st.session_state.experiment_log.index + 1, st.session_state.experiment_log['성장률'], marker='o')
    ax.set_xlabel("실험 횟수")
    ax.set_ylabel("성장률")
    ax.set_title("실험 횟수에 따른 식물 성장률 변화")
    ax.grid(True)
    st.pyplot(fig)

    # 각 변수와 성장률의 상관관계 그래프
    st.subheader("📊 변인과 성장률의 관계")
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    ax1.scatter(st.session_state.experiment_log['빛'], st.session_state.experiment_log['성장률'])
    ax1.set_xlabel("빛의 세기")
    ax1.set_ylabel("성장률")
    ax1.set_title("빛 vs 성장률")
    ax1.grid(True)

    ax2.scatter(st.session_state.experiment_log['물'], st.session_state.experiment_log['성장률'])
    ax2.set_xlabel("물의 양")
    ax2.set_ylabel("성장률")
    ax2.set_title("물 vs 성장률")
    ax2.grid(True)

    ax3.scatter(st.session_state.experiment_log['CO2'], st.session_state.experiment_log['성장률'])
    ax3.set_xlabel("이산화탄소 농도")
    ax3.set_ylabel("성장률")
    ax3.set_title("CO2 vs 성장률")
    ax3.grid(True)

    st.pyplot(fig)


# --- 정답 확인 (목표 변경에 맞춰 수정된 부분) ---
st.subheader("🕵️‍♂️ 추론 및 정답 확인")
col_guess1, col_guess2 = st.columns(2)

with col_guess1:
    guess_variable = st.radio(
        "어떤 변인이 비밀 변인일까요?",
        ['빛의 세기', '물의 양', '이산화탄소 농도']
    )

with col_guess2:
    guess_value = st.number_input(
        "그 변인의 100% 성장 지점은 몇일까요?",
        min_value=1, max_value=10, value=5, step=1 # 입력 범위 변경
    )


if st.button("정답 확인!"):
    secret_var_korean = {
        'light': '빛의 세기',
        'water': '물의 양',
        'co2': '이산화탄소 농도'
    }

    is_variable_correct = (guess_variable == secret_var_korean.get(st.session_state.secret_variable))
    is_value_correct = (guess_value == st.session_state.optimal_value)

    if is_variable_correct and is_value_correct:
        st.balloons()
        st.success(f"🎉 **정답입니다!** 비밀 변인은 **{guess_variable}**였고, 최적의 값은 **{st.session_state.optimal_value}**였습니다!")
        st.write(f"**과학적 설명:** {get_scientific_explanation(st.session_state.secret_variable)}")
    elif is_variable_correct and not is_value_correct:
        st.error(f"❌ 비밀 변인은 맞췄지만, 최적의 값은 틀렸네요. 그래프에서 성장률이 가장 높은 지점을 찾아보세요!")
    elif not is_variable_correct and is_value_correct:
        st.error(f"❌ 값은 맞췄지만, 비밀 변인은 틀렸네요. 어떤 변인이 성장률에 가장 큰 영향을 주었는지 다시 분석해 보세요.")
    else:
        st.error(f"❌ 아쉽네요. 다시 한번 실험 결과를 분석해 보세요.")

    st.write("---")
    st.write("새로운 게임을 시작하려면 앱을 새로고침(F5)하세요.")
