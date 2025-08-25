import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import os

# --- 페이지 설정 ---
st.set_page_config(
    page_title="광합성 탐정: 비밀 변인을 찾아라!",
    layout="wide"
)

st.title("🌱 광합성 탐정: 비밀 변인을 찾아라!")
st.write("여러분의 임무는 식물의 성장에 가장 큰 영향을 미치는 '비밀 변인'을 찾아내는 것입니다. 빛, 물, 이산화탄소 중 하나를 조작하여 실험을 반복하고, 데이터를 분석해 보세요!")

# --- 세션 상태 초기화 ---
if 'secret_variable' not in st.session_state:
    st.session_state.secret_variable = random.choice(['light', 'water', 'co2'])
    st.session_state.experiment_log = pd.DataFrame(columns=['빛', '물', 'CO2', '성장률'])
    st.session_state.max_growth = random.uniform(50, 100) # 최대 성장률을 무작위로 설정

# --- UI 요소 ---
st.subheader("🧪 실험 조건 설정")
col1, col2, col3 = st.columns(3)

with col1:
    light_level = st.slider("☀️ 빛의 세기 (%)", 0, 100, 50)
with col2:
    water_level = st.slider("💧 물의 양 (mL)", 0, 100, 50)
with col3:
    co2_level = st.slider("💨 이산화탄소 농도 (ppm)", 0, 100, 50)

# --- 실험 결과 계산 함수 ---
def calculate_growth(light, water, co2, secret_var, max_growth):
    growth_rate = 0
    if secret_var == 'light':
        # 빛의 세기에 따라 성장률 변화 (2차 함수 형태)
        growth_rate = -0.01 * (light - 50)**2 + 100
    elif secret_var == 'water':
        # 물의 양에 따라 성장률 변화 (2차 함수 형태)
        growth_rate = -0.01 * (water - 50)**2 + 100
    elif secret_var == 'co2':
        # CO2 농도에 따라 성장률 변화 (2차 함수 형태)
        growth_rate = -0.01 * (co2 - 50)**2 + 100

    # 0보다 작거나 100보다 큰 값은 조정
    growth_rate = max(0, min(100, growth_rate))

    # 다른 변수들의 영향 (노이즈) 추가
    noise_factor = 0.5
    if secret_var != 'light':
        growth_rate -= noise_factor * abs(light - 50) / 5
    if secret_var != 'water':
        growth_rate -= noise_factor * abs(water - 50) / 5
    if secret_var != 'co2':
        growth_rate -= noise_factor * abs(co2 - 50) / 5

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

    # --- 식물 성장 그림 표시 (추가된 부분) ---
    st.subheader("🌱 식물 성장 모습")
    if current_growth < 25:
        image_path = "plant_stage1.png" # 식물 성장 초기 단계 이미지
        growth_text = "🌱 아직 성장이 미미합니다."
    elif current_growth < 50:
        image_path = "plant_stage2.png" # 식물 성장 중간 단계 이미지
        growth_text = "🌿 조금씩 자라고 있네요!"
    elif current_growth < 75:
        image_path = "plant_stage3.png" # 식물 성장 활발한 단계 이미지
        growth_text = "🌳 제법 많이 자랐어요!"
    else:
        image_path = "plant_stage4.png" # 식물 최대 성장 단계 이미지
        growth_text = "🌲 매우 건강하게 잘 자랐습니다!"

    st.write(growth_text)
    if os.path.exists(image_path):
        st.image(image_path, caption=f"현재 성장률: {current_growth}", use_column_width=True)
    else:
        st.error(f"이미지 파일 '{image_path}'을 찾을 수 없습니다! 스크립트와 같은 폴더에 이미지 파일을 넣어주세요.")

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


# --- 정답 확인 ---
st.subheader("🕵️‍♂️ 추론 및 정답 확인")
guess_variable = st.radio(
    "어떤 변인이 식물의 성장에 가장 큰 영향을 미쳤을까요?",
    ['빛의 세기', '물의 양', '이산화탄소 농도']
)

if st.button("정답 확인!"):
    secret_var_korean = {
        'light': '빛의 세기',
        'water': '물의 양',
        'co2': '이산화탄소 농도'
    }

    if guess_variable == secret_var_korean.get(st.session_state.secret_variable):
        st.balloons()
        st.success(f"🎉 **정답입니다!** 비밀 변인은 바로 **{guess_variable}**였습니다!")
        st.write(f"**과학적 설명:** {get_scientific_explanation(st.session_state.secret_variable)}")
    else:
        st.error(f"❌ 아쉽네요. 다시 한번 실험 결과를 분석해 보세요.")
        st.info(f"힌트: {get_hint(st.session_state.secret_variable)}")

    st.write("---")
    st.write("새로운 게임을 시작하려면 앱을 새로고침(F5)하세요.")


def get_scientific_explanation(secret_var):
    explanations = {
        'light': "빛은 광합성에 필요한 에너지를 제공합니다. 빛의 세기가 증가하면 광합성 속도가 빨라져 식물 성장이 촉진되지만, 너무 강한 빛은 오히려 성장을 저해할 수 있습니다.",
        'water': "물은 광합성 반응의 필수적인 재료입니다. 물이 충분해야 이산화탄소가 잎으로 흡수되고, 물 분해가 일어나 에너지를 얻을 수 있습니다.",
        'co2': "이산화탄소는 광합성을 통해 포도당을 만드는 데 사용되는 주요 원료입니다. 이산화탄소 농도가 높을수록 광합성 속도가 빨라집니다."
    }
    return explanations.get(secret_var, "알 수 없는 변인입니다.")

def get_hint(secret_var):
    hints = {
        'light': "가로축이 '빛의 세기'인 그래프를 자세히 살펴보세요. 성장률이 어떤 패턴으로 변하는지 알 수 있을 거예요.",
        'water': "가로축이 '물의 양'인 그래프를 보면 다른 변인들과는 다른 뚜렷한 경향을 보일 거예요.",
        'co2': "이산화탄소 농도에 따른 성장률 변화가 가장 뚜렷하게 나타날 겁니다. 해당 그래프를 다시 확인해 보세요."
    }
    return hints.get(secret_var, "다시 실험을 진행하며 데이터를 더 모아보세요.")
