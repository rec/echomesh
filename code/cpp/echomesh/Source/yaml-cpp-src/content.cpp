#include "content.h"
#include "yaml-cpp/node.h"
#include <cassert>

namespace YAML
{
	void Content::SetData(const std::string&)
	{
		assert(false);
	}

	void Content::Append(std::auto_ptr<Node>)
	{
		assert(false);
	}

	void Content::Insert(std::auto_ptr<Node>, std::auto_ptr<Node>)
	{
		assert(false);
	}
}
