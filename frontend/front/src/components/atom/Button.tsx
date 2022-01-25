import { memo, VFC } from "react";

type ChildProps = {
  children: string;
  RedirectPath: () => void;
};

export const Button: VFC<ChildProps> = memo(({ children, RedirectPath }) => {
  return (
    <button
      onClick={RedirectPath}
      className="bg-transparent border-2 border-white-200 hover:bg-white hover:text-red-500 text-white font-bold py-5 px-12 rounded-full"
    >
      {children}
    </button>
  );
});
