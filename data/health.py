"""
Health protocol data including mobility exercises for all phases and sessions.
"""

from typing import Dict, List, Any
from datetime import datetime

def get_mobility_phase1() -> Dict[str, List[Dict[str, Any]]]:
    """Return Phase 1 (Months 1-6) mobility protocol data."""
    return {
        "morning": [
            {
                "name": "Dynamic Cat-Cow",
                "sets_reps": "2 mins",
                "equipment": "None",
                "notes": "Mobilize the entire spine. Inhale to arch, exhale to round."
            },
            {
                "name": "Dynamic Leg Swings",
                "sets_reps": "15 reps/side",
                "equipment": "None",
                "notes": "Front/back and lateral swings. Prioritize controlled motion."
            },
            {
                "name": "90/90 Hip Switch",
                "sets_reps": "10 reps/side",
                "equipment": "None",
                "notes": "Improve internal/external hip rotation. Keep pelvis neutral."
            },
            {
                "name": "Baddha Konasana (PNF)",
                "sets_reps": "3x30s hold",
                "equipment": "Yoga blocks",
                "notes": "Contract hips inward for 5s, relax deeper. Critical for lotus progression."
            },
            {
                "name": "Half-Lotus Prep with Band",
                "sets_reps": "2x30s/side",
                "equipment": "Resistance band",
                "notes": "Gently traction foot into external rotation. Avoid knee pain."
            },
            {
                "name": "Quadruped Thoracic Rotation",
                "sets_reps": "10 reps/side",
                "equipment": "None",
                "notes": "Enhance spinal rotation for twists like Marichyasana. Exhale into rotation."
            },
            {
                "name": "Seated Wide-Legged Forward Fold",
                "sets_reps": "2x45s",
                "equipment": "Yoga strap",
                "notes": "Targets adductors for Upavistha Konasana. Keep knees bent if tight."
            },
            {
                "name": "Supported Bridge Pose",
                "sets_reps": "2x60s",
                "equipment": "Yoga block",
                "notes": "Passive thoracic extension for backbend prep. Block under sacrum."
            },
            {
                "name": "Foam Roller IT Band Release",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller",
                "notes": "Slow rolling + pauses. Avoid bony areas."
            },
            {
                "name": "Dynamic Pigeon Pose",
                "sets_reps": "8 reps/side",
                "equipment": "None",
                "notes": "Pulse gently to open hips. Focus on glute/hip flexor mobility."
            },
            {
                "name": "Scapular Wall Slides",
                "sets_reps": "3x10 reps",
                "equipment": "Wall",
                "notes": "Improve shoulder/scapular control for arm balances."
            },
            {
                "name": "Supine Spinal Twist",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Release lower back tension. Keep shoulders grounded."
            }
        ],
        "lunch": [
            {
                "name": "Wall Angels",
                "sets_reps": "3x10 reps",
                "equipment": "Wall",
                "notes": "Enhances scapular control and thoracic extension. Keep lower back flat."
            },
            {
                "name": "Chair-Assisted Thoracic Extension",
                "sets_reps": "2x8 reps",
                "equipment": "Office chair",
                "notes": "Arch upper back over chair edge. Prepares for Urdhva Dhanurasana."
            },
            {
                "name": "Median Nerve Glides",
                "sets_reps": "8–10 reps/arm",
                "equipment": "None",
                "notes": "Gentle nerve mobilization for thoracic/shoulder health. No pain."
            },
            {
                "name": "Bent-Knee Eccentric Sliders",
                "sets_reps": "3x10 reps/side",
                "equipment": "Chair/sliders",
                "notes": "Rehab for hamstring tendinopathy. Control eccentric phase."
            },
            {
                "name": "Side-Lying Thoracic Opener",
                "sets_reps": "2x45s/side",
                "equipment": "Yoga block",
                "notes": "Stretch chest/shoulders. Block under ribcage for support."
            },
            {
                "name": "Standing Forward Fold (Bent Knee)",
                "sets_reps": "2x60s",
                "equipment": "Yoga strap",
                "notes": "Safe hamstring stretch. Keep knees bent to protect tendons."
            },
            {
                "name": "Kettlebell Goblet Cossack Squat",
                "sets_reps": "2x6 reps/side",
                "equipment": "20kg kettlebell",
                "notes": "Loaded hip mobility for Utthita Parsvakonasana. Go slow."
            },
            {
                "name": "Diaphragmatic Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Activates parasympathetic nervous system. Inhale 4s, exhale 6s."
            },
            {
                "name": "Scapular Push-Ups",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Strengthen serratus anterior for shoulder stability."
            },
            {
                "name": "Prone Cobra",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Strengthen spinal extensors. Lift chest and legs while squeezing glutes."
            },
            {
                "name": "Foam Roll Thoracic Spine",
                "sets_reps": "2 mins",
                "equipment": "Foam roller",
                "notes": "Roll mid-back to improve extension."
            },
            {
                "name": "Child's Pose with Side Reach",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Stretch lats and improve thoracic rotation."
            }
        ],
        "pre_bed": [
            {
                "name": "Nordic Curl Negatives",
                "sets_reps": "3x5 reps",
                "equipment": "Resistance band",
                "notes": "Eccentric hamstring rehab. Lower slowly (3–5s)."
            },
            {
                "name": "PNF Pancake Stretch",
                "sets_reps": "3x30s",
                "equipment": "Yoga blocks",
                "notes": "Contract adductors for 5s, relax deeper. Blocks under knees if needed."
            },
            {
                "name": "IT Band Massage Gun Therapy",
                "sets_reps": "2 mins/side",
                "equipment": "Massage gun",
                "notes": "Glide along lateral thigh. Avoid direct pressure on bone."
            },
            {
                "name": "Supported Reclined Hero Pose",
                "sets_reps": "2x60s",
                "equipment": "Yoga chair",
                "notes": "Stretch quads/hip flexors. Use chair for depth control."
            },
            {
                "name": "Legs-Up-The-Wall + Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Enhances circulation and parasympathetic tone."
            },
            {
                "name": "Infrared Mat Therapy",
                "sets_reps": "10 mins",
                "equipment": "Infrared/NIR mat",
                "notes": "Boosts tissue healing. Focus on lower back/hips."
            },
            {
                "name": "Yin Yoga Frog Pose",
                "sets_reps": "3x90s",
                "equipment": "Yoga blocks",
                "notes": "Passive adductor stretch. Blocks under knees for support."
            },
            {
                "name": "Supine Bound Angle",
                "sets_reps": "5 mins",
                "equipment": "Strap",
                "notes": "Passive hip/internal rotation stretch. Strap around thighs for support."
            },
            {
                "name": "Lacrosse Ball Glute Release",
                "sets_reps": "2 mins/side",
                "equipment": "Lacrosse ball",
                "notes": "Target gluteus medius/minimus for hip stability."
            },
            {
                "name": "Gentle Neck Release",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Tilt head side-to-side to relieve tension."
            },
            {
                "name": "Alternate Nostril Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Balance the nervous system and reduce stress."
            }
        ]
    }

def get_mobility_phase2() -> Dict[str, List[Dict[str, Any]]]:
    """Return Phase 2 (Months 7-12) mobility protocol data."""
    return {
        "morning": [
            {
                "name": "Sun Salutation A (Full Vinyasa)",
                "sets_reps": "5 rounds",
                "equipment": "None",
                "notes": "Link breath to movement. Focus on smooth transitions."
            },
            {
                "name": "Lizard Pose with PNF",
                "sets_reps": "3x30s/side",
                "equipment": "Yoga blocks",
                "notes": "Contract front hip into block for 5s, relax deeper. Targets Hanumanasana prep."
            },
            {
                "name": "Marichyasana C Prep",
                "sets_reps": "3x30s/side",
                "equipment": "Strap",
                "notes": "Loop strap around foot and opposite hip to simulate bind. Rotate spine actively."
            },
            {
                "name": "Kettlebell Overhead Squat Hold",
                "sets_reps": "3x20s/side",
                "equipment": "20kg kettlebell",
                "notes": "Loaded shoulder/hip mobility for Utkatasana. Keep core braced."
            },
            {
                "name": "Dolphin Push-Ups",
                "sets_reps": "3x8 reps",
                "equipment": "None",
                "notes": "Strengthen shoulders and core for Pincha Mayurasana. Lower chest toward floor."
            },
            {
                "name": "Standing Splits (Active Pulses)",
                "sets_reps": "3x10 pulses/side",
                "equipment": "Wall",
                "notes": "Build hamstring strength in lengthened position. Avoid bouncing."
            },
            {
                "name": "Kapotasana Prep (Wall Walk)",
                "sets_reps": "3x5 reps",
                "equipment": "Wall",
                "notes": "Walk hands down wall into backbend. Tuck ribs to protect lumbar spine."
            },
            {
                "name": "Dynamic Spinal Waves",
                "sets_reps": "2 mins",
                "equipment": "None",
                "notes": "Flow between cat-cow and cobra for segmental spinal control."
            },
            {
                "name": "PNF Pancake Stretch with Kettlebell",
                "sets_reps": "3x30s",
                "equipment": "20kg kettlebell",
                "notes": "Press knees outward gently for adductor flexibility. Avoid strain."
            },
            {
                "name": "Foam Roller IT Band Release",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller",
                "notes": "Reduce lateral thigh stiffness. Roll slowly with pauses."
            },
            {
                "name": "Scapular Wall Slides",
                "sets_reps": "3x10 reps",
                "equipment": "Wall",
                "notes": "Strengthen serratus anterior for shoulder stability in arm balances."
            },
            {
                "name": "Supine Leg Circles",
                "sets_reps": "10 reps/side",
                "equipment": "None",
                "notes": "Improve hip joint mobility for Supta Kurmasana. Keep pelvis stable."
            }
        ],
        "lunch": [
            {
                "name": "Camel Pose (Dynamic Pulses)",
                "sets_reps": "3x8 reps",
                "equipment": "None",
                "notes": "Pulse into backbend with hands on heels. Focus on thoracic extension."
            },
            {
                "name": "Scapular Push-Ups",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Strengthen serratus anterior for Bakasana and arm balances."
            },
            {
                "name": "Bow Pose with PNF",
                "sets_reps": "3x20s hold",
                "equipment": "Strap",
                "notes": "Contract glutes/hamstrings for 5s, relax deeper. Use strap if needed."
            },
            {
                "name": "Side Crow Prep",
                "sets_reps": "3x5 reps/side",
                "equipment": "Yoga blocks",
                "notes": "Shift weight forward onto hands, knees on blocks. Build lateral core strength."
            },
            {
                "name": "Bridge Pose to Wheel",
                "sets_reps": "3x5 reps",
                "equipment": "Yoga block",
                "notes": "Lift from bridge to wheel pose. Use block under sacrum for support."
            },
            {
                "name": "Forearm Stand Drills",
                "sets_reps": "3x30s hold",
                "equipment": "Wall",
                "notes": "Kick up to forearm stand against wall. Engage core and shoulders."
            },
            {
                "name": "Nadi Shodhana Breathwork",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Alternate nostril breathing to balance energy for intense backbends."
            },
            {
                "name": "Thoracic Release with Ball",
                "sets_reps": "2 mins",
                "equipment": "Lacrosse ball",
                "notes": "Target rhomboids and mid-traps. Roll slowly between shoulder blades."
            },
            {
                "name": "Prone T-Spine Extension",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Lift chest and arms while squeezing scapulae. Strengthen spinal extensors."
            },
            {
                "name": "Standing Quad Stretch with PNF",
                "sets_reps": "2x30s/side",
                "equipment": "Wall",
                "notes": "Contract quads against wall for 5s, then relax deeper."
            },
            {
                "name": "Seated Spinal Twist",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Improve rotational mobility for Marichyasana D. Exhale into the twist."
            },
            {
                "name": "Child's Pose with Side Reach",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Stretch lats and improve thoracic rotation."
            }
        ],
        "pre_bed": [
            {
                "name": "Yin Yoga Pigeon Pose",
                "sets_reps": "3x90s/side",
                "equipment": "Bolster",
                "notes": "Passive hip opener with forward fold. Bolster under knee if needed."
            },
            {
                "name": "Supported Fish Pose",
                "sets_reps": "3x60s",
                "equipment": "Bolster/blanket",
                "notes": "Stretch anterior thoracic spine. Place bolster vertically under spine."
            },
            {
                "name": "Eccentric Nordic Curls",
                "sets_reps": "3x6 reps",
                "equipment": "Resistance band",
                "notes": "Lower over 5s, assist up. Maintain hamstring tendon resilience."
            },
            {
                "name": "Adductor Ball Release",
                "sets_reps": "2 mins/side",
                "equipment": "Lacrosse ball",
                "notes": "Release inner thighs for splits and leg-behind-head poses."
            },
            {
                "name": "Supine Spinal Twist with Traction",
                "sets_reps": "3x60s/side",
                "equipment": "Strap",
                "notes": "Use strap to gently pull knee toward floor while grounding shoulders."
            },
            {
                "name": "Legs-Up-The-Wall w/ Pelvic Tilts",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Enhance circulation and decompress lumbar spine."
            },
            {
                "name": "Infrared Mat + Visualization",
                "sets_reps": "10 mins",
                "equipment": "Infrared/NIR mat",
                "notes": "Pair heat therapy with mental rehearsal of complex asanas."
            },
            {
                "name": "Yin Yoga Dragon Pose",
                "sets_reps": "2x90s/side",
                "equipment": "Yoga blocks",
                "notes": "Deep hip flexor stretch. Blocks under hands for support."
            },
            {
                "name": "Gentle Neck Release",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Tilt head side-to-side to relieve tension."
            },
            {
                "name": "Alternate Nostril Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Balance the nervous system and reduce stress."
            },
            {
                "name": "Foam Roll Glutes/Hamstrings",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller",
                "notes": "Roll posterior chain to release tension from weightlifting."
            }
        ]
    }

def get_mobility_phase3() -> Dict[str, List[Dict[str, Any]]]:
    """Return Phase 3 (Advanced) mobility protocol data."""
    return {
        "morning": [
            {
                "name": "Sun Salutation B (Full Vinyasa)",
                "sets_reps": "5 rounds",
                "equipment": "None",
                "notes": "Link breath to movement. Emphasize jump-backs and jump-throughs."
            },
            {
                "name": "Kapotasana Prep with Bands",
                "sets_reps": "3x30s hold",
                "equipment": "Resistance bands",
                "notes": "Loop bands around thighs to engage glutes while deepening backbend."
            },
            {
                "name": "Dwi Pada Sirsasana Drills",
                "sets_reps": "3x30s/side",
                "equipment": "Yoga blocks",
                "notes": "Elevate hips with blocks to reduce strain. Work toward full pose."
            },
            {
                "name": "Handstand Push-Up Negatives",
                "sets_reps": "3x5 reps",
                "equipment": "Wall",
                "notes": "Lower slowly from handstand to build shoulder stability."
            },
            {
                "name": "Marichyasana D Prep",
                "sets_reps": "3x30s/side",
                "equipment": "Strap",
                "notes": "Loop strap around foot and opposite hip to mimic bind mechanics."
            },
            {
                "name": "Dynamic Spinal Waves",
                "sets_reps": "2 mins",
                "equipment": "None",
                "notes": "Flow between cat-cow and cobra for segmental control."
            },
            {
                "name": "PNF Pancake with Weight",
                "sets_reps": "3x30s",
                "equipment": "20kg kettlebell",
                "notes": "Press knees outward for adductor flexibility. Avoid strain."
            },
            {
                "name": "IT Band + Glute Release",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller/massage gun",
                "notes": "Target TFL and glute medius for leg-behind-head poses."
            },
            {
                "name": "Scapular Wall Slides",
                "sets_reps": "3x10 reps",
                "equipment": "Wall",
                "notes": "Strengthen serratus anterior for shoulder stability."
            },
            {
                "name": "Drop-Backs with Spotter",
                "sets_reps": "5 reps",
                "equipment": "Strap/Wall",
                "notes": "Standing to Urdhva Dhanurasana with controlled eccentric."
            },
            {
                "name": "L-Sit to Compass Pose",
                "sets_reps": "3x8 reps/side",
                "equipment": "None",
                "notes": "Strengthen hip flexors and obliques for advanced poses."
            },
            {
                "name": "Supine Leg Circles",
                "sets_reps": "10 reps/side",
                "equipment": "None",
                "notes": "Improve hip mobility for Supta Kurmasana."
            }
        ],
        "lunch": [
            {
                "name": "Weighted Back Extensions",
                "sets_reps": "3x10 reps",
                "equipment": "24kg kettlebell",
                "notes": "Hold kettlebell to chest. Strengthen erectors for backbends."
            },
            {
                "name": "Advanced Crow to Handstand",
                "sets_reps": "3x5 reps",
                "equipment": "Yoga blocks",
                "notes": "Transition from Bakasana to handstand. Build explosive power."
            },
            {
                "name": "Bow Pose with PNF",
                "sets_reps": "3x30s hold",
                "equipment": "Strap",
                "notes": "Contract glutes/hamstrings, then deepen backbend."
            },
            {
                "name": "Rotator Cuff Drills",
                "sets_reps": "3x15 reps/side",
                "equipment": "Resistance band",
                "notes": "External/internal rotations for shoulder health."
            },
            {
                "name": "Kapalabhati Breathwork",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Skull-shining breath for energy and focus."
            },
            {
                "name": "Thoracic Release",
                "sets_reps": "2 mins",
                "equipment": "Lacrosse ball",
                "notes": "Target rhomboids and mid-traps for mobility."
            },
            {
                "name": "Prone T-Spine Extension",
                "sets_reps": "3x10 reps",
                "equipment": "None",
                "notes": "Strengthen spinal extensors for backbends."
            },
            {
                "name": "Standing Quad PNF",
                "sets_reps": "2x30s/side",
                "equipment": "Wall",
                "notes": "Contract quads, then deepen stretch."
            },
            {
                "name": "Forearm Stand to Scorpion",
                "sets_reps": "3x30s hold",
                "equipment": "Wall",
                "notes": "Lift one leg toward head in forearm stand."
            },
            {
                "name": "Dynamic Dragon Pose",
                "sets_reps": "8 reps/side",
                "equipment": "None",
                "notes": "Pulse in lunge to open hip flexors."
            },
            {
                "name": "Seated Spinal Twist",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Improve rotation for advanced twists."
            },
            {
                "name": "Child's Pose with Side Reach",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Release lats and thoracic spine."
            }
        ],
        "pre_bed": [
            {
                "name": "Yin Dragon Pose",
                "sets_reps": "3x90s/side",
                "equipment": "Bolster",
                "notes": "Deep hip flexor stretch with forward fold."
            },
            {
                "name": "Supported Kapotasana",
                "sets_reps": "3x60s",
                "equipment": "Yoga chair",
                "notes": "Rest forearms on chair for safe backbend."
            },
            {
                "name": "Eccentric Nordic Curls",
                "sets_reps": "3x8 reps",
                "equipment": "Resistance band",
                "notes": "6s lowering phase for hamstring health."
            },
            {
                "name": "Adductor Release",
                "sets_reps": "2 mins/side",
                "equipment": "Lacrosse ball",
                "notes": "Release inner thighs for advanced poses."
            },
            {
                "name": "Spinal Twist with Traction",
                "sets_reps": "3x60s/side",
                "equipment": "Strap",
                "notes": "Use strap to deepen twist safely."
            },
            {
                "name": "Legs-Up-Wall",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Decompress spine and enhance circulation."
            },
            {
                "name": "Infrared Therapy",
                "sets_reps": "10 mins",
                "equipment": "Infrared/NIR mat",
                "notes": "Heat therapy with pose visualization."
            },
            {
                "name": "Yin Sphinx Pose",
                "sets_reps": "3x90s",
                "equipment": "Bolster",
                "notes": "Passive thoracic extension with support."
            },
            {
                "name": "Neck Release",
                "sets_reps": "1 min/side",
                "equipment": "None",
                "notes": "Gentle side-to-side tilts."
            },
            {
                "name": "Alternate Nostril Breathing",
                "sets_reps": "5 mins",
                "equipment": "None",
                "notes": "Balance nervous system before sleep."
            },
            {
                "name": "Foam Roll Release",
                "sets_reps": "2 mins/side",
                "equipment": "Foam roller",
                "notes": "Release posterior chain tension."
            },
            {
                "name": "Supported Shoulderstand",
                "sets_reps": "3x60s",
                "equipment": "Wall",
                "notes": "Decompress spine with wall support."
            }
        ]
    }

def get_current_phase() -> str:
    """Return the current mobility training phase."""
    return "Phase 2"  # This can be updated based on progress

def get_current_session() -> str:
    """Return the current session based on time of day."""
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "morning"
    elif 11 <= hour < 17:
        return "lunch"
    else:
        return "pre_bed"

def get_phase_exercises(phase: str, session: str) -> List[Dict[str, Any]]:
    """Get exercises for a specific phase and session."""
    phase_data = {
        "Phase 1": get_mobility_phase1(),
        "Phase 2": get_mobility_phase2(),
        "Phase 3": get_mobility_phase3()
    }
    return phase_data[phase][session]

def get_current_exercises() -> List[Dict[str, Any]]:
    """Get the current exercises based on phase and time of day."""
    current_phase = get_current_phase()
    current_session = get_current_session()
    return get_phase_exercises(current_phase, current_session) 