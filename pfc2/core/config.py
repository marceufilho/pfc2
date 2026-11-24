"""Named toolchain, experiment defaults and bounded I/O limits."""

DEFAULT_CLANG = "clang-19"
CLANG_ENV_VAR = "PFC_CLANG"
PROCESS_TIMEOUT_SECONDS = 10
# The last two silence lint about source that is odd but defined (`g = g;`, `n != n`); the released C keeps what
# the source wrote, and a certified program must not fail to build for it.
C_FLAGS = ("-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-Wno-self-assign", "-Wno-tautological-compare")
MAX_SOURCE_BYTES = 1_048_576
MAX_PREPROCESSED_BYTES = 8_388_608
MAX_AST_DEPTH = 200
MAX_AST_NODES = 50_000
MAX_VC_TERM_NODES = 5_000_000
MAX_VC_TERM_DEPTH = 100
SOLVER_TIMEOUT_MS = 10_000
MAX_SOLVER_TIMEOUT_MS = 60_000

MAX_SOLVER_CACHE_ENTRIES = 4096
MAX_VC_PATHS = 256
MAX_REPORT_BYTES = 64 * 1024 * 1024
OPENAI_KEY_ENV = "OPENAI_API_KEY"
PROPOSER_ATTEMPTS = 5
MAX_PROMPT_BYTES = 65536
MAX_PROPOSAL_BYTES = 16384
