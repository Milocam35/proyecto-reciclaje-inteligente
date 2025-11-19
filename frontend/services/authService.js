import {
  signIn,
  signOut,
  signUp,
  getCurrentUser,
  fetchAuthSession,
} from "aws-amplify/auth";


// ===============================
// LOGIN
// ===============================
export const login = async (username, password) => {
  try {
    await signIn({ username, password });

    // Usuario básico
    const user = await getCurrentUser();

    // Sesión para obtener atributos del token
    const session = await fetchAuthSession();
    const payload = session.tokens?.idToken?.payload || {};

    return {
      ok: true,
      user: {
        username: user.username,
        userId: user.userId,

        // Atributos del usuario
        email: payload.email || null,
        name: payload.name || null,
        role: payload["custom:usuario"] || null,
        sub: payload.sub || null,
      },
    };

  } catch (err) {
    return { ok: false, message: err.message };
  }
};


// ===============================
// LOGOUT
// ===============================
export const logout = async () => {
  console.log("Logging out...");
  await signOut();
};


// ===============================
// REGISTER
// ===============================
export const register = async (username, password, email) => {
  try {
    const result = await signUp({
      username,
      password,
      options: {
        userAttributes: {
          email,
        },
      },
    });
    return { ok: true, data: result };
  } catch (err) {
    return { ok: false, message: err.message };
  }
};


// ===============================
// CURRENT USER
// ===============================
export const currentUser = async () => {
  try {
    const user = await getCurrentUser();
    const session = await fetchAuthSession();

    const payload = session.tokens?.idToken?.payload || {};

    return {
      username: user.username,
      userId: user.userId,

      // Atributos ampliados
      email: payload.email || null,
      name: payload.name || null,
      role: payload["custom:usuario"] || null,
      sub: payload.sub || null,
    };

  } catch {
    return null; // no hay usuario
  }
};
